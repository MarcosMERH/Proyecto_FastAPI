
document.querySelector(".d-grid gap-2").addEventListener("click", e => {
    if (e.target.classList.contains('btn btn-outline-primary')) {
        // Realiza las operaciones necesarias con los datos (por ejemplo, obtener valores de otros campos)
        console.log('Click de: Edit');
    }
    if (e.target.classList.contains('btn btn-outline-danger')) {
        // Realiza las operaciones necesarias con los datos (por ejemplo, obtener valores de otros campos)
        console.log('Click de: Delete');  
    }
});