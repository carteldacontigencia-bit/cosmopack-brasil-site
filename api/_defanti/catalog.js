import { readFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
let _catalog = null;

export function getCatalog() {
  if (!_catalog) {
    const raw = readFileSync(resolve(__dirname, '../../catalog.json'), 'utf8');
    _catalog = JSON.parse(raw);
  }
  return _catalog;
}

export function findProduct(id) {
  return getCatalog().products.find(p => p.id === id) || null;
}

export function calcTotal(items) {
  const catalog = getCatalog();
  let total = 0;
  for (const item of items) {
    const product = findProduct(item.id);
    if (!product) throw new Error(`Produto não encontrado: ${item.id}`);
    let price = product.price;
    if (item.variant && product.variants) {
      const v = product.variants.options.find(o => o.id === item.variant);
      if (v && typeof v.price === 'number') price = v.price;
    }
    total += price * item.qty;
  }
  return total;
}

export function calcShipping(items) {
  const catalog = getCatalog();
  const count = items.reduce((n, it) => n + it.qty, 0);
  const tiers = catalog.shipping.tiers;
  let best = tiers[0];
  for (const t of tiers) {
    if (count >= t.minItems && t.minItems >= best.minItems) best = t;
  }
  return best;
}

export function cors(res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
}
