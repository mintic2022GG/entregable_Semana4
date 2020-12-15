window.onload = iniciar; 

function iniciar() {
    document.getElementById("Recuperar").addEventListener('click', validar, false);
}

function validaUsername(){
    var elemento = document.getElementById("username").value;
    if( elemento === null || elemento.length === 0 || /^\s+$/.test(elemento) ) {
        alert('[ERROR] El campo debe tener algun valor');
        return false;
    }
    return true;
}


function validar(e) {
    if (validaUsername() && confirm("Pulsa aceptar si deseas enviar el formulario")) {
        return true;
    } else {
        e.preventDefault();
        return false;
    }
}
