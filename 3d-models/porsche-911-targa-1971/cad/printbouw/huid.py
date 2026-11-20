"""Maak een gesloten offset rond de originele oppervlakken. Alle coördinaten in mm."""
import numpy as np
from numba import njit
from scipy import ndimage
from skimage.measure import marching_cubes
import manifold3d as mf


@njit(inline="always")
def edge_distance(px, py, pz, dx, dy, dz):
    length = dx*dx + dy*dy + dz*dz
    t = min(1., max(0., (px*dx + py*dy + pz*dz) / max(length, 1.e-20)))
    return (px-t*dx)**2 + (py-t*dy)**2 + (pz-t*dz)**2


@njit
def trace(grid, triangles, radius, pitch, origin):
    # Afstand tot het projectievlak binnen de driehoek, anders tot de rand.
    margin = radius + 1.7*pitch
    for tri in triangles:
        a,b,c = tri
        ab,ac,bc = b-a,c-a,c-b
        normal = np.cross(ab, ac)
        area = np.dot(normal,normal)
        if area < 1.e-16:
            continue
        nx,ny,nz = normal / np.sqrt(area)
        inward = np.cross(normal, ab), np.cross(normal, bc), np.cross(normal,-ac)
        lower = np.maximum(0, np.ceil((np.minimum(np.minimum(a,b),c)-margin-origin)/pitch).astype(np.int64))
        upper = np.minimum(np.array(grid.shape)-1, np.floor((np.maximum(np.maximum(a,b),c)+margin-origin)/pitch).astype(np.int64))
        for i in range(lower[0],upper[0]+1):
            x = origin[0]+i*pitch
            for j in range(lower[1],upper[1]+1):
                y = origin[1]+j*pitch
                for k in range(lower[2],upper[2]+1):
                    z = origin[2]+k*pitch
                    px,py,pz = x-a[0], y-a[1], z-a[2]
                    plane = px*nx+py*ny+pz*nz
                    current = grid[i,j,k]+radius
                    if abs(plane) >= current:
                        continue
                    qx,qy,qz = x-b[0], y-b[1], z-b[2]
                    rx,ry,rz = x-c[0], y-c[1], z-c[2]
                    ea,eb,ec = inward
                    if (px*ea[0]+py*ea[1]+pz*ea[2]>=0 and
                        qx*eb[0]+qy*eb[1]+qz*eb[2]>=0 and rx*ec[0]+ry*ec[1]+rz*ec[2]>=0):
                        dist = abs(plane)
                    else:
                        dist = np.sqrt(min(edge_distance(px,py,pz,ab[0],ab[1],ab[2]),
                                           edge_distance(qx,qy,qz,bc[0],bc[1],bc[2]),
                                           edge_distance(rx,ry,rz,-ac[0],-ac[1],-ac[2])))
                    if dist < current:
                        grid[i,j,k] = dist-radius


def surface(groups, pitch):
    lower = np.min([tris.min(axis=(0,1))-r for tris,r in groups],axis=0)
    upper = np.max([tris.max(axis=(0,1))+r for tris,r in groups],axis=0)
    origin = (np.floor(lower/pitch)-3)*pitch
    shape = np.ceil((upper-origin)/pitch).astype(int)+4
    grid = np.full(shape,2*pitch,dtype=np.float32)
    for tris,radius in groups:
        trace(grid,tris,radius,pitch,origin)
    # Alleen ingesloten luchtholten vullen. Cockpit, wielkasten en onderkant blijven open.
    outside=grid>0
    closed=ndimage.binary_fill_holes(~outside)
    grid[closed & outside]=-pitch
    # Bij smalle spleten kan het nulniveau exact door een rasterpunt gaan.
    v,f,_,_=marching_cubes(grid,level=.000137,spacing=(pitch,)*3,allow_degenerate=False)
    mesh=mf.Mesh(np.asarray(v+origin,np.float32),np.ascontiguousarray(f[:,::-1],np.uint32))
    mesh.merge()
    part=mf.Manifold(mesh)
    if part.volume()<0:
        mesh=mf.Mesh(np.asarray(v+origin,np.float32),np.ascontiguousarray(f,np.uint32))
        mesh.merge()
        part=mf.Manifold(mesh)
    if part.status()!=mf.Error.NoError:
        raise ValueError(part.status())
    return part.simplify(.045)


def regularize(part, pitch, inset=0.):
    """Herbemonster gesneden randen. De afstand komt van het snijresultaat zelf."""
    import vtk
    from vtk.util.numpy_support import numpy_to_vtk, numpy_to_vtkIdTypeArray, vtk_to_numpy
    mesh=part.to_mesh64()
    v=np.asarray(mesh.vert_properties[:,:3],float)
    f=np.asarray(mesh.tri_verts,dtype=np.int64)
    origin=(np.floor(v.min(axis=0)/pitch)-3.271)*pitch
    shape=np.ceil((v.max(axis=0)-origin)/pitch).astype(int)+4
    points=vtk.vtkPoints();points.SetData(numpy_to_vtk(v,deep=True))
    cells=vtk.vtkCellArray()
    offsets=numpy_to_vtkIdTypeArray(np.arange(0,3*len(f)+1,3,dtype=np.int64),deep=True)
    cells.SetData(offsets,numpy_to_vtkIdTypeArray(f.ravel(),deep=True))
    poly=vtk.vtkPolyData();poly.SetPoints(points);poly.SetPolys(cells)
    stencil=vtk.vtkPolyDataToImageStencil()
    stencil.SetInputData(poly);stencil.SetOutputOrigin(*origin);stencil.SetOutputSpacing(*([pitch]*3))
    stencil.SetOutputWholeExtent(0,shape[0]-1,0,shape[1]-1,0,shape[2]-1)
    mask=vtk.vtkImageStencilToImage();mask.SetInputConnection(stencil.GetOutputPort())
    mask.SetInsideValue(1);mask.SetOutsideValue(0);mask.SetOutputScalarTypeToUnsignedChar();mask.Update()
    inside=vtk_to_numpy(mask.GetOutput().GetPointData().GetScalars()).reshape(tuple(shape),order='F')
    field=np.full(shape,2*pitch,dtype=np.float32)
    trace(field,v[f],0.,pitch,origin)
    field[inside!=0]*=-1
    ndimage.gaussian_filter(field,.63,output=field)
    verts,faces,_,_=marching_cubes(field,level=.000137-inset,spacing=(pitch,)*3,allow_degenerate=False)
    mesh=mf.Mesh64(np.ascontiguousarray(verts+origin,np.float64),np.ascontiguousarray(faces,np.uint64))
    mesh.merge()
    obj=mf.Manifold(mesh)
    assert obj.volume()>0 and obj.status()==mf.Error.NoError,(obj.status(),obj.volume())
    return obj.as_original().simplify(.035)
