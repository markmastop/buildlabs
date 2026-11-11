"""Genereer de v17-STL met trimesh en manifold3d."""
from pathlib import Path
import sys
import trimesh
from manifold3d import Mesh, Manifold

base = Path(__file__).with_name('truma_bracket_base_v10.stl')
out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('truma_bracket_v17.stl')
src = trimesh.load_mesh(base, process=True)
body = Manifold(Mesh(src.vertices.astype('float32'), src.faces.astype('uint32')))

# Cable entry is on the side opposite the Truma button: lower edge y=0.
# Radius 5.5 mm, opening Ø11 mm. No other edits.
tool_mesh = trimesh.creation.cylinder(
    radius=5.5, height=8.0, sections=128,
    transform=trimesh.transformations.translation_matrix([39.0, 0.0, 1.5])
)
tool = Manifold(Mesh(tool_mesh.vertices.astype('float32'), tool_mesh.faces.astype('uint32')))
body = body - tool
mm = body.to_mesh()
result = trimesh.Trimesh(vertices=mm.vert_properties[:, :3], faces=mm.tri_verts, process=False)
result.export(out)
print('status', body.status(), 'faces', len(result.faces), 'bounds', result.bounds.tolist())
