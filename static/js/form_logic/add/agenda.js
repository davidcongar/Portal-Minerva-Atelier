document.getElementById("dynamic_form").addEventListener("submit", async function (e) {
  e.preventDefault();

  const form = e.target;
  const hora_inicio = document.getElementById("hora_inicio").value;
  const fecha = document.getElementById("fecha").value;

  const hora_min = "09:00";
  const hora_max = "17:00";

  const day = new Date(fecha).getUTCDay();
  const isWeekend = (day === 0 || day === 6);

  if (isWeekend) {
    showAlert('Favor de seleccionar una fecha entre lunes y viernes.');
    return;
  }

  if (hora_inicio < hora_min || hora_inicio > hora_max) {
    showAlert('Favor de registrar un horario entre 9:00am y 5:00pm.');
    return;
  }

  form.querySelectorAll(':disabled').forEach(el => {
    el.disabled = false;
  });
  form.submit();
});
