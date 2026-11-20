// Lees de getransformeerde driehoeken uit dezelfde scène als de projectpagina.
const {chromium}=require('playwright');
const fs=require('node:fs'), path=require('node:path'), {pathToFileURL}=require('node:url');
async function main() {
  const dest=process.argv[2];
  if (!dest) throw new Error('Gebruik: node lees-viewer.cjs <werkmap>');
  fs.mkdirSync(dest,{recursive:true});
  const browser=await chromium.launch({executablePath:process.env.CHROME_BIN || undefined,
    args:['--use-angle=swiftshader','--enable-unsafe-swiftshader']});
  try {
    const page=await browser.newPage();
    const libs=process.env.THREE_R128;
    if(libs) await page.route('https://**/*',route=>{
      const url=route.request().url();
      const local=url.endsWith('three.min.js')?libs:url.endsWith('OrbitControls.js')?process.env.ORBIT_R128:null;
      return local?route.fulfill({path:local,contentType:'text/javascript'}):route.abort();
    });
    await page.goto(pathToFileURL(path.resolve(__dirname,'../../index.html')).href,{waitUntil:'domcontentloaded'});
    await page.waitForFunction(()=>window.__targa);
    const names=await page.evaluate(()=>{
      const car=window.__targa.scene.getObjectByName('Targa'), gear=car.getObjectByName('Studieonderstel');
      const roof=window.__targa.roof, cockpit=car.getObjectByName('Interieur');
      car.updateMatrixWorld(true);
      // De viewer kan de hele kap in de samengebouwde stand verschuiven.
      const local=new THREE.Matrix4().copy(car.matrixWorld).invert();
      const parts=new Map();
      function collect(obj,part) {
        obj.traverse(o=>{
          if(!o.isMesh)return;
          let group=o.userData.printPart||part;
          if(group==='overslaan')return;
          if(o.material.vertexColors)group='huid';
          const g=o.geometry, pos=g.attributes.position, colors=g.attributes.color;
          const matrix=new THREE.Matrix4().multiplyMatrices(local,o.matrixWorld);
          const vec=new THREE.Vector3(), pts=[];
          for(let i=0;i<pos.count;i++){
            vec.fromBufferAttribute(pos,i).applyMatrix4(matrix);
            pts.push([.1*vec.x,-.1*vec.z,.1*vec.y]);
          }
          const arr=parts.get(group)||[]; parts.set(group,arr);
          const idx=g.index?g.index.array:null;
          for(let k=0;k<(idx?idx.length:pos.count);k+=3) {
            const face=idx?[idx[k],idx[k+1],idx[k+2]]:[k,k+1,k+2];
            if(group==='huid' && face.some(i=>colors.getX(i)<.4))continue;
            for(const i of face) arr.push(...pts[i]);
          }
        });
      }
      const wheels=gear.children.filter(o=>o.isGroup);
      if(wheels.length!==4)throw Error('Vier studiewielen verwacht');
      collect(wheels[0],'wiel-voor'); collect(wheels[2],'wiel-achter');
      gear.children.filter(o=>!o.isGroup).forEach(o=>collect(o,'uitlaat'));
      for(const o of car.children)if(o!==gear)
        collect(o,o===roof?'dak':o===cockpit?'interieur':o.userData.printPart||'details');
      window.printMeshes=parts; return [...parts.keys()];
    });
    for(const name of names){
      const encoded=await page.evaluate(n=>{
        const b=new Uint8Array(Float32Array.from(window.printMeshes.get(n)).buffer);
        let s=''; for(let i=0;i<b.length;i+=32768)s+=String.fromCharCode(...b.subarray(i,i+32768));
        return btoa(s);
      },name);
      const data=Buffer.from(encoded,'base64'); fs.writeFileSync(path.join(dest,name+'.tri'),data);
      console.log(name,data.length/36,'driehoeken');
    }
  }finally{await browser.close();}
}
main().catch(e=>{console.error(e);process.exitCode=1;});
