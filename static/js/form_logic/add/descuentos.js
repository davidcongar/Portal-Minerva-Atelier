document.getElementById("dynamic_form").addEventListener("submit", async function (e) {
    e.preventDefault();

    const form = e.target;
    const id_servicio = document.getElementById("id_servicio").value.trim();
    const id_espacio = document.getElementById("id_espacio").value.trim();
    const codigo_de_descuento = document.getElementById("codigo_de_descuento").value.trim();

    if ((id_servicio && !id_espacio) || (!id_servicio && id_espacio)) {
        showAlert('Debe seleccionar ambos: servicio y espacio.');
        return;
    }
    if (id_servicio && id_espacio){
        try {
            const response = await fetch(
                `/descuentos/validate/${id_espacio}/${id_servicio}`,
                {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": "{{ csrf_token() }}",
                    },
                }
            );
            const data = await response.json();
            if (data.status === "warning" && data.message) {
                showAlert(data.message);
                return;
            }
        } catch (err) {
            console.error("Error:", err);
        }
    }
    try {
        const response = await fetch(
            `/descuentos/validate_code/${codigo_de_descuento}`,
            {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": "{{ csrf_token() }}",
                },
            }
        );
        const data = await response.json();
        if (data.status === "warning" && data.message) {
            showAlert(data.message);
            return;
        }
    } catch (err) {
        console.error("Error:", err);
    }

  form.querySelectorAll(':disabled').forEach(el => {
    el.disabled = false;
  });

  form.submit();
});