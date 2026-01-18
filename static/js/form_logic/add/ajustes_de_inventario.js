document.getElementById("cantidad").addEventListener("change", async function () {
    const tipo = document.getElementById("tipo_de_ajuste")?.value;
    const cantidad = document.getElementById("cantidad");
    const caducidad = document.getElementById("caducidad");
    const id_almacen = document.getElementById("id_almacen")?.value;
    const id_producto = document.getElementById("id_producto")?.value;

    if (!tipo) return; // Extra protection

    // Only apply logic if type = "Salida"
    if (tipo === "Salida") {

        const cantidad_ingresada = cantidad.value || "";

        // Validate almacen & producto selected
        if (!id_almacen || !id_producto) {
            cantidad.value = ""; // input should be empty, not null

            showAlert("Favor de ingresar el almacén y el producto");
            return;
        }

        // Call backend for validation
        try {
            const response = await fetch(
                `/ajustes_de_inventario/revision_salida/${id_almacen}/${id_producto}/${cantidad_ingresada}`,
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
                cantidad.value = "";
                showAlert(data.message);
            }
        } catch (err) {
            console.error("Error:", err);
        }
    }
});
