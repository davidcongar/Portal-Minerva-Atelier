document.getElementById("dynamic_form").addEventListener("submit", async function (e) {
  e.preventDefault();

  const form = e.target;
  const salida = document.getElementById("id_cuenta_de_banco_salida").value;
  const entrada = document.getElementById("id_cuenta_de_banco_entrada").value;


  if (salida === entrada) {
    showAlert('La cuenta de banco de salida no puede ser igual a la cuenta de banco de entrada. Favor de revisar.');
    return;
  }

  form.querySelectorAll(':disabled').forEach(el => {
    el.disabled = false;
  });
  form.submit();
});
