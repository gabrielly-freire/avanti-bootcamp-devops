const fmtCurrency = (v) =>
  new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(v || 0);

async function api(path, opts = {}) {
  const res = await fetch(path, {
    headers: { 'Content-Type': 'application/json' },
    ...opts,
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || `Erro HTTP ${res.status}`);
  }
  if (res.status === 204) return null;
  return res.json();
}

async function loadMedicines() {
  const tbody = document.querySelector('#table-medicines tbody');
  tbody.innerHTML = '<tr><td colspan="7">Carregando...</td></tr>';
  const data = await api('/api/medicamentos');
  tbody.innerHTML = '';
  data.forEach((m) => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${m.id}</td>
      <td>${m.nome}</td>
      <td>${m.fabricante}</td>
      <td>${m.validade ? new Date(m.validade).toLocaleDateString() : '-'}</td>
      <td class="text-end">${fmtCurrency(m.preco)}</td>
      <td class="text-end">${m.estoque}</td>
      <td class="text-end">
        <div class="btn-group btn-group-sm">
          <button class="btn btn-outline-primary btn-edit">Editar</button>
          <button class="btn btn-outline-danger btn-del">Excluir</button>
        </div>
      </td>
    `;
    tr.querySelector('.btn-edit').addEventListener('click', () => fillForm(m));
    tr.querySelector('.btn-del').addEventListener('click', async () => {
      if (confirm(`Excluir ${m.nome}?`)) {
        try {
          await api(`/api/medicamentos/${m.id}`, { method: 'DELETE' });
          await loadMedicines();
          await refreshMedSelect();
        } catch (e) { alert(e.message); }
      }
    });
    tbody.appendChild(tr);
  });
}

function clearForm() {
  document.getElementById('med-id').value = '';
  document.getElementById('med-nome').value = '';
  document.getElementById('med-fabricante').value = '';
  document.getElementById('med-validade').value = '';
  document.getElementById('med-preco').value = '';
  document.getElementById('med-estoque').value = '';
  document.getElementById('med-rx').checked = false;
}

function fillForm(m) {
  document.getElementById('med-id').value = m.id;
  document.getElementById('med-nome').value = m.nome;
  document.getElementById('med-fabricante').value = m.fabricante;
  document.getElementById('med-validade').value = m.validade ? m.validade.substring(0,10) : '';
  document.getElementById('med-preco').value = m.preco;
  document.getElementById('med-estoque').value = m.estoque;
}

let basket = [];
function updateCartTable() {
  const tbody = document.querySelector('#table-cart tbody');
  tbody.innerHTML = '';
  let total = 0;
  basket.forEach((item, idx) => {
    const tr = document.createElement('tr');
    const subtotal = item.preco_unitario * item.quantidade;
    total += subtotal;
    tr.innerHTML = `
      <td>${item.nome}</td>
      <td class="text-end">${item.quantidade}</td>
      <td class="text-end">${fmtCurrency(item.preco_unitario)}</td>
      <td class="text-end">${fmtCurrency(subtotal)}</td>
      <td class="text-end"><button class="btn btn-sm btn-outline-danger">Remover</button></td>
    `;
    tr.querySelector('button').addEventListener('click', () => {
      basket.splice(idx, 1);
      updateCartTable();
    });
    tbody.appendChild(tr);
  });
  document.getElementById('cart-total').textContent = fmtCurrency(total);
}

async function refreshMedSelect() {
  const meds = await api('/api/medicamentos');
  const sel = document.getElementById('sale-med');
  sel.innerHTML = '';
  meds.forEach((m) => {
    const opt = document.createElement('option');
    opt.value = m.id;
    opt.textContent = `${m.nome} (${fmtCurrency(m.preco)}) - estoque: ${m.estoque}`;
    opt.dataset.preco = m.preco;
    opt.dataset.nome = m.nome;
    sel.appendChild(opt);
  });
}

document.addEventListener('DOMContentLoaded', async () => {
  document.getElementById('btn-add-medicine').addEventListener('click', clearForm);
  document.getElementById('btn-clear').addEventListener('click', clearForm);

  document.getElementById('form-medicine').addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
      nome: document.getElementById('med-nome').value,
      fabricante: document.getElementById('med-fabricante').value,
      validade: document.getElementById('med-validade').value || null,
      preco: parseFloat(document.getElementById('med-preco').value || '0'),
      estoque: parseInt(document.getElementById('med-estoque').value || '0', 10),
      receita_obrigatoria: document.getElementById('med-rx').checked,
    };
    const id = document.getElementById('med-id').value;
    try {
      if (id) {
        await api(`/api/medicamentos/${id}`, { method: 'PUT', body: JSON.stringify(payload) });
      } else {
        await api('/api/medicamentos', { method: 'POST', body: JSON.stringify(payload) });
      }
      clearForm();
      await loadMedicines();
      await refreshMedSelect();
    } catch (e) {
      alert(e.message);
    }
  });

  document.getElementById('sale-add').addEventListener('click', () => {
    const sel = document.getElementById('sale-med');
    const qtd = parseInt(document.getElementById('sale-qtd').value || '1', 10);
    if (!sel.value) return;
    const preco = parseFloat(sel.selectedOptions[0].dataset.preco);
    const nome = sel.selectedOptions[0].dataset.nome;
    basket.push({
      medicamento_id: parseInt(sel.value, 10),
      quantidade: qtd,
      preco_unitario: preco,
      nome,
    });
    updateCartTable();
  });
  document.getElementById('sale-clear').addEventListener('click', () => {
    basket = [];
    updateCartTable();
  });
  document.getElementById('sale-finish').addEventListener('click', async () => {
    if (!basket.length) { alert('Carrinho vazio'); return; }
    try {
      const sale = await api('/api/vendas', { method: 'POST', body: JSON.stringify({ itens: basket }) });
      alert(`Venda #${sale.id} total: ${fmtCurrency(sale.total)}`);
      basket = [];
      updateCartTable();
      await loadMedicines();
      await refreshMedSelect();
      await loadSales();
    } catch (e) { alert(e.message); }
  });

  await loadMedicines();
  await refreshMedSelect();
  await loadSales();
});

async function loadSales() {
  const ul = document.getElementById('sales-list');
  ul.innerHTML = '';
  const vendas = await api('/api/vendas');
  vendas.forEach((v) => {
    const li = document.createElement('li');
    li.className = 'list-group-item d-flex justify-content-between';
    const dt = new Date(v.criado_em).toLocaleString();
    li.innerHTML = `<span>#${v.id} • ${dt} • itens: ${v.itens.length}</span><strong>${fmtCurrency(v.total)}</strong>`;
    ul.appendChild(li);
  });
}
