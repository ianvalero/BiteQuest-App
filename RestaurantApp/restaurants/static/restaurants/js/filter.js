document.querySelectorAll("#categories_filter button").forEach(button => {
    console.log(button.dataset);
    button.addEventListener("click", () => {
        // Alterna entre 'enabled' y 'disabled'
        button.classList.toggle("enabled");
        button.classList.toggle("disabled");

        // Actualiza el campo oculto con las categorías deshabilitadas
        const disabledCategories = Array.from(
            document.querySelectorAll("#categories_filter button.disabled")
        ).map(btn => btn.dataset.category);

        document.querySelector("#disabled_categories").value = disabledCategories.join(",");
    });
});

// Resetea los filtros y clases al hacer clic en "Reset"
document.querySelector("#reset_filters").addEventListener("click", () => {
    document.querySelectorAll("#categories_filter button").forEach(button => {
        button.classList.remove("disabled");
        button.classList.add("enabled");
    });
    document.querySelector("#disabled_categories").value = "";
    document.querySelector("#search").value = "";
});