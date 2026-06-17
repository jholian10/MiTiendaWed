let datosColombia = [];

document.addEventListener("DOMContentLoaded", function() {
    const urlGist = 'https://gist.githubusercontent.com/jholian10/89b363329953127fde6ff570a3c85a23/raw/c86c5ac08969771f80ae64e09b966d99ab716c2e/gistfile1.txt'; 
    
    fetch(urlGist)
        .then(response => response.json())
        .then(data => {
            datosColombia = data;
            const selectDepto = document.getElementById('departamento');
            
            selectDepto.innerHTML = '<option value="">Selecciona un departamento</option>';

            data.forEach(item => {
                const opt = document.createElement('option');
                opt.value = item.departamento; 
                opt.textContent = item.departamento;
                selectDepto.appendChild(opt);
            });
        })
        .catch(err => console.error("Error al cargar JSON de departamentos:", err));
});

function cargarMunicipios() {
    const deptoSeleccionado = document.getElementById('departamento').value;
    const selectCiudad = document.getElementById('ciudad');
    
    selectCiudad.innerHTML = '<option value="">Selecciona un municipio</option>';
    
    const infoDepto = datosColombia.find(item => item.departamento === deptoSeleccionado);
    
    if (infoDepto && infoDepto.ciudades) {
        infoDepto.ciudades.forEach(ciudad => {
            const opt = document.createElement('option');
            opt.value = ciudad;
            opt.textContent = ciudad;
            selectCiudad.appendChild(opt);
        });
    }
}
