/* Servidor de desarrollo: sirve public/ y enruta /api/* a los handlers,
   como haría Vercel. */
import http from 'node:http';
import fs from 'node:fs';
process.env.XPAG_BASE_URL='http://127.0.0.1:8787';
process.env.XPAG_CLIENT_ID='test_id';
process.env.XPAG_CLIENT_SECRET='test_secret';
process.env.XPAG_WEBHOOK_URL='http://127.0.0.1:8080/api/webhook';
const DIR='../public';
const rutas={
  '/api/checkout': (await import('../api/checkout.js')).default,
  '/api/status':   (await import('../api/status.js')).default,
  '/api/webhook':  (await import('../api/webhook.js')).default,
};
http.createServer(async (req,res)=>{
  const u=new URL(req.url,'http://x');
  const h=rutas[u.pathname];
  if(h){
    req.query=Object.fromEntries(u.searchParams);
    const original={setHeader:res.setHeader.bind(res)};
    res.status=(c)=>{res.statusCode=c;return res;};
    res.json=(o)=>{original.setHeader('Content-Type','application/json');res.end(JSON.stringify(o));return res;};
    return h(req,res);
  }
  const f=u.pathname==='/'||u.pathname==='/checkout'?'/checkout.html':u.pathname;
  try{
    const buf=fs.readFileSync(DIR+f);
    res.writeHead(200,{'Content-Type':f.endsWith('.html')?'text/html; charset=utf-8':'application/octet-stream'});
    res.end(buf);
  }catch{ res.writeHead(404); res.end('no'); }
}).listen(8080,()=>console.log('dev en :8080'));
