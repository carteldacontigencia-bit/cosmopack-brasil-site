/* Mock del API de XPag con las respuestas EXACTAS de la documentación.
   Existe porque api.xpag.global no es alcanzable desde el entorno de
   build. Puerto 8787. */
import http from 'node:http';

const pagos = new Map();  // transaction_id -> registro
const porExterno = new Map();

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, 'http://x');
  const trozos = [];
  for await (const c of req) trozos.push(c);
  const body = trozos.length ? JSON.parse(Buffer.concat(trozos).toString()) : {};
  const json = (code, obj) => {
    res.writeHead(code, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(obj));
  };

  if (!req.headers['x-client-id'] || !req.headers['x-client-secret']) {
    return json(401, { ok: false, error: 'Credenciais ausentes.', error_code: 'missing_credentials' });
  }

  if (url.pathname === '/cashin' && req.method === 'POST') {
    if (body.currency !== 'MXN') return json(400, { ok: false, error_code: 'currency_not_supported' });
    if (typeof body.amount !== 'number') return json(422, { ok: false, error_code: 'invalid_amount' });

    const esOxxo = body.method === 'OXXO';
    if (esOxxo && body.amount < 10) return json(422, { ok: false, error_code: 'amount_below_min' });
    if (esOxxo && body.amount > 10000) return json(422, { ok: false, error_code: 'amount_above_limit' });

    const id = (esOxxo ? 'oxxo_' : 'pr_') + Math.random().toString(36).slice(2, 10);
    const reg = {
      id, status: 'pending', amount: body.amount, currency: 'MXN',
      external_id: body.external_id, e2e: 'E' + id.toUpperCase(),
      webhook_url: body.webhook_url || null,
      payer_name: body.name || body.payerData?.name || null,
    };
    pagos.set(id, reg);
    if (body.external_id) porExterno.set(body.external_id, reg);

    if (esOxxo) {
      return json(200, {
        ok: true, currency: 'MXN', amount: body.amount, fee: 5, method: 'OXXO',
        request_number: id, transaction_id: id, status: 'pending',
        awaiting_instruction: false, transfer_type: 'REFERENCE',
        payee_data: {
          transferType: 'REFERENCE',
          reference: '8204240000119882',
          barcode: 'https://static.muwe.mx/abc.png',
        },
      });
    }
    return json(200, {
      ok: true, reference: 'REF123456', clabe: '012345678901234567',
      amount: body.amount, fee: 5, currency: 'MXN',
      request_number: id, transaction_id: id, status: 'pending',
      bank_name: 'STP (Sistema de Transferencia y Pagos)', beneficiary: 'Zypher',
    });
  }

  if (url.pathname === '/consult-transaction' && req.method === 'GET') {
    const tx = url.searchParams.get('transaction_id') || url.searchParams.get('request_number');
    const ext = url.searchParams.get('external_id');
    if (tx) {
      const p = pagos.get(tx);
      if (!p) return json(404, { ok: false, error_code: 'deposit_not_found' });
      return json(200, {
        ok: true, type: 'cashin', status: p.status, amount: p.amount, fee: 5,
        currency: p.currency, request_number: tx, transaction_id: tx,
        e2e: p.e2e, external_id: p.external_id, payer_name: p.payer_name,
        provider: 'XPag',
      });
    }
    if (ext) {
      const p = porExterno.get(ext);
      if (!p) return json(404, { ok: false, error_code: 'deposit_not_found' });
      /* Por external_id la documentación devuelve LISTA. */
      return json(200, {
        ok: true, type: 'cashin', count: 1,
        payments: [{
          id: p.id, status: p.status, amount: p.amount, fee: 5, currency: p.currency,
          e2e: p.e2e, transaction_id: p.id, external_id: ext,
          clabe: '012345678901234567', payer_name: p.payer_name || 'Prueba',
        }],
      });
    }
    return json(400, { ok: false, error_code: 'missing_reference' });
  }

  if (url.pathname === '/balance') {
    return json(200, { ok: true, balances: { MXN: { available: 9999, blocked: 0 } } });
  }

  /* Atajo de prueba: marcar pagado y avisar al webhook, como hace
     /sandbox/simulate en el sandbox real. */
  if (url.pathname === '/__simular' && req.method === 'POST') {
    const p = pagos.get(body.transaction_id) || porExterno.get(body.external_id);
    if (!p) return json(404, { ok: false });
    p.status = body.outcome === 'paid' ? 'confirmed' : (body.outcome || 'failed');
    if (p.webhook_url) {
      try {
        await fetch(p.webhook_url, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            type: 'cashin', status: p.status === 'confirmed' ? 'confirmed' : p.status,
            amount: p.amount, fee: 5, currency: 'MXN',
            request_number: p.id, transaction_id: p.id,
            external_id: p.external_id, e2e: p.e2e, provider: 'XPag',
          }),
        });
      } catch { /* el test comprueba el webhook por separado */ }
    }
    return json(200, { ok: true, status: p.status });
  }

  json(404, { ok: false, error_code: 'not_found' });
});

server.listen(8787, () => console.log('mock XPag en :8787'));
