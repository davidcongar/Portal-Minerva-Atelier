document.getElementById("dynamic_form").addEventListener("submit", async function (e) {
  e.preventDefault();

  const form = e.target;
  const salida = document.getElementById("id_almacen_salida").value;
  const entrada = document.getElementById("id_almacen_entrada").value;


  if (salida === entrada) {
    showAlert('El almacén de salida no puede ser igual al almacén de entrada. Favor de revisar.');
    return;
  }

  form.querySelectorAll(':disabled').forEach(el => {
    el.disabled = false;
  });
  form.submit();
});
