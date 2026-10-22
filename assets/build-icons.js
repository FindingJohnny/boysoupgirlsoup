// Renders apple-touch-icon.png and og.png from favicon.svg. Run from the repo root: node assets/build-icons.js
// Needs Playwright (npm i -g playwright); set HTTPS_PROXY if the fonts have to come through a proxy.
const fs=require("fs"),path=require("path");
const pw=require(require("child_process").execSync("npm root -g").toString().trim()+"/playwright");
const dir=__dirname,svg=fs.readFileSync(path.join(dir,"favicon.svg"),"utf8");
const bowl=svg.replace(/<rect[^>]*\/>/,""); // drop the rounded tile, the pages below draw their own background
const fonts='<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Shrikhand&family=Figtree:wght@600&display=block">';
(async()=>{
  const args=process.env.HTTPS_PROXY?["--proxy-server="+process.env.HTTPS_PROXY]:[];
  const b=await pw.chromium.launch({args});
  const p=await b.newPage();
  // iOS rounds the corners itself, so the touch icon is a full square.
  await p.setViewportSize({width:180,height:180});
  await p.setContent('<body style="margin:0;background:#fdf4e3">'+bowl.replace("<svg ",'<svg width="180" height="180" ')+"</body>");
  await p.screenshot({path:path.join(dir,"apple-touch-icon.png")});
  await p.setViewportSize({width:1200,height:630});
  await p.setContent(fonts+`<body style="margin:0;width:1200px;height:630px;display:flex;align-items:center;justify-content:center;gap:48px;
    background:#fdf4e3;border-bottom:18px solid;border-image:linear-gradient(90deg,#d9577a 50%,#2f557f 50%) 1;box-sizing:border-box">
    ${bowl.replace("<svg ",'<svg width="300" height="300" ')}
    <div style="font-family:Shrikhand;font-size:96px;line-height:1.02">
      <div style="color:#d9577a">Girl Soup,</div><div style="color:#2f557f">Boy Soup</div>
      <div style="font:600 34px Figtree,sans-serif;color:#66707f;margin-top:22px">Two phones. Twenty soups. Who knows soup?</div>
    </div></body>`,{waitUntil:"networkidle"});
  await p.evaluate(()=>document.fonts.ready);
  await p.screenshot({path:path.join(dir,"og.png")});
  await b.close();
})();
