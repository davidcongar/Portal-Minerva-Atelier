$('#id_espacio').on('change', async function () {
    const id_espacio = document.getElementById("id_espacio")?.value;
    const id_servicio = document.getElementById("id_servicio")?.value;

    if (!id_espacio || !id_servicio) return;

    try {
        const response = await fetch(
            `/precios_de_servicios/validate/${id_espacio}/${id_servicio}`,
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
            $("#id_espacio").val("").trigger("change");
            showAlert(data.message);
        }
    } catch (err) {
        console.error("Error:", err);
    }
});