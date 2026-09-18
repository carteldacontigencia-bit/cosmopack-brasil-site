/* Mock del endpoint de la Conversions API de Meta. Guarda lo recibido
   para que la prueba pueda inspeccionarlo. Puerto 8788. */
import http from 'node:http';

export const recibidos = [];

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, 'http://x');
  const trozos = [];
  for await (const c of req) trozos.push(c);
  const body = trozos.length ? JSON.parse(Buffer.concat(trozos).toString()) : {};

  if (url.pathname === '/__recibidos') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    return res.end(JSON.stringify(recibidos));
  }
  if (url.pathname === '/__limpiar') {
    recibidos.length = 0;
    res.writeHead(200); return res.end('{}');
  }

  const m = url.pathname.match(/^\/v\d+\.\d+\/(\d+)\/events$/);
  if (m && req.method === 'POST') {
    if (!body.access_token) {
      res.writeHead(400, { 'Content-Type': 'application/json' });
      return res.end(JSON.stringify({ error: { message: 'falta access_token' } }));
    }
    recibidos.push({ pixelId: m[1], ...body });
    res.writeHead(200, { 'Content-Type': 'application/json' });
    return res.end(JSON.stringify({ events_received: body.data.length, fbtrace_id: 'mock' }));
  }
  res.writeHead(404); res.end('{}');
});

server.listen(8788, () => console.log('mock Meta en :8788'));
