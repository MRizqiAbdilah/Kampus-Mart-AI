const token = localStorage.getItem("token"); // misal token JWT dari login

async function topupSaldo() {
  const jumlah = document.getElementById("topup-amount").value;
  const res = await fetch("/saldo/topup?jumlah=" + jumlah, {
    method: "POST",
    headers: {
      Authorization: "Bearer " + token,
    },
  });

  const data = await res.json();
  const qrisDiv = document.getElementById("qris-topup");
  if (data.qris_image_base64) {
    qrisDiv.innerHTML = `
      <p>${data.message}</p>
      <img src="data:image/png;base64,${data.qris_image_base64}" />
      <button onclick="confirmTopup(${jumlah})">Konfirmasi Pembayaran</button>
    `;
  } else {
    qrisDiv.innerHTML = `<p>${data.detail || JSON.stringify(data)}</p>`;
  }
}

async function confirmTopup(jumlah) {
  const res = await fetch("/saldo/confirm?jumlah=" + jumlah, {
    method: "POST",
    headers: { Authorization: "Bearer " + token },
  });
  const data = await res.json();
  alert(data.message || JSON.stringify(data));
}

async function beliProduk() {
  const produk_id = document.getElementById("produk-id").value;
  const jumlah = document.getElementById("jumlah").value;
  const res = await fetch("/transaksi", {
    method: "POST",
    headers: {
      Authorization: "Bearer " + token,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ produk_id, jumlah }),
  });

  const data = await res.json();
  const qrisDiv = document.getElementById("qris-transaksi");

  if (data.qris_image_base64) {
    qrisDiv.innerHTML = `
      <p>${data.message}</p>
      <img src="data:image/png;base64,${data.qris_image_base64}" />
      <button onclick="confirmQris(${data.transaksi_id})">Konfirmasi Pembayaran QRIS</button>
    `;
  } else {
    qrisDiv.innerHTML = `<p>Transaksi berhasil via saldo ✅</p>`;
  }
}

async function confirmQris(id) {
  const res = await fetch("/qris/confirm/" + id, {
    method: "POST",
    headers: { Authorization: "Bearer " + token },
  });
  const data = await res.json();
  alert(data.message || JSON.stringify(data));
}
