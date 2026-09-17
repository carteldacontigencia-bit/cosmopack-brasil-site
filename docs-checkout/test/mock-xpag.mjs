/* Mock del API de XPag con las respuestas EXACTAS de la documentación.
   Sirve para probar los handlers, ya que api.xpag.global está bloqueado
   por el proxy de este entorno. */
import http from 'node:http';
const pagos = new Map();

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, 'http://x');
  const trozos = []; for await (const c of req) trozos.push(c);
  const body = trozos.length ? JSON.parse(Buffer.concat(trozos).toString()) : {};
  const json = (code, obj) => { res.writeHead(code, {'Content-Type':'application/json'}); res.end(JSON.stringify(obj)); };

  if (!req.headers['x-client-id'] || !req.headers['x-client-secret'])
    return json(401, { ok:false, error:'Credenciais ausentes.', error_code:'missing_credentials' });

  if (url.pathname === '/cashin' && req.method === 'POST') {
    if (body.currency !== 'MXN') return json(400, { ok:false, error_code:'currency_not_supported' });
    const id = 'pr_' + Math.random().toString(36).slice(2,10);
    pagos.set(id, { external_id: body.external_id, amount: body.amount, status:'pending', currency:'MXN' });
    pagos.set(body.external_id, { id, ...pagos.get(id) });
    if (body.method === 'OXXO') {
      if (body.amount < 10) return json(422, { ok:false, error:'Valor abaixo do mínimo.', error_code:'amount_below_min' });
      if (body.amount > 10000) return json(422, { ok:false, error_code:'amount_above_limit' });
      return json(200, { ok:true, currency:'MXN', amount:body.amount, fee:5, method:'OXXO',
        request_number:id, transaction_id:id, status:'pending', awaiting_instruction:false,
        transfer_type:'REFERENCE',
        payee_data:{ transferType:'REFERENCE', reference:'8204240000119882', barcode:'https://static.muwe.mx/abc.png' } });
    }
    return json(200, { ok:true, reference:'REF123456', clabe:'012345678901234567', amount:body.amount,
      fee:5, currency:'MXN', request_number:id, transaction_id:id, status:'pending',
      bank_name:'STP (Sistema de Transferencia y Pagos)', beneficiary:'Zypher' });
  }

  if (url.pathname === '/consult-transaction' && req.method === 'GET') {
    const tx = url.searchParams.get('transaction_id') || url.searchParams.get('request_number');
    const ext = url.searchParams.get('external_id');
    if (tx) {
      const p = pagos.get(tx);
      if (!p) return json(404, { ok:false, error_code:'deposit_not_found' });
      return json(200, { ok:true, type:'cashin', status:p.status, amount:p.amount, fee:5,
        request_number:tx, transaction_id:tx, e2e:'E'+tx, external_id:p.external_id, provider:'XPag' });
    }
    if (ext) {
      const p = pagos.get(ext);
      if (!p) return json(404, { ok:false, error_code:'deposit_not_found' });
      return json(200, { ok:true, type:'cashin', count:1, payments:[
        { id:p.id, status:p.status, amount:p.amount, fee:5, currency:'MXN', e2e:'E'+p.id,
          transaction_id:p.id, external_id:ext, clabe:'012345678901234567' } ] });
    }
    return json(400, { ok:false, error_code:'missing_reference' });
  }

  /* atajo de la prueba: marcar pagado */
  if (url.pathname === '/__pagar' && req.method === 'POST') {
    const p = pagos.get(body.transaction_id);
    if (!p) return json(404, {ok:false});
    p.status = 'confirmed';
    const ep = pagos.get(p.external_id); if (ep) ep.status = 'confirmed';
    return json(200, {ok:true});
  }
  json(404, { ok:false, error_code:'not_found' });
});
server.listen(8787, () => console.log('mock en :8787'));
