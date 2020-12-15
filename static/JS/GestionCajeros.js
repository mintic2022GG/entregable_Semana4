window.onload = iniciar; 

function iniciar() {
    document.getElementById("Agregar").addEventListener('click', validar, false);
}

function validaNombre(){
    var elemento = document.getElementById("Nombre").value;
    if( elemento === null || elemento.length === 0 || /^\s+$/.test(elemento) ) {
        alert('[ERROR] El campo debe tener algun valor');
        return false;
        }    
    return true;
}

function validaCedula(){
    var elemento = document.getElementById("Cedula").value;
    if( elemento === null || elemento.length === 0 || /^\s+$/.test(elemento) ) {
        alert('[ERROR] El campo debe tener algun valor');
        return false;
    }
    if( isNaN(elemento) ) {
        alert('[ERROR] El campo debe tener un valor numerico');    
        return false;
    }
    return true;
}

function validaCorreo(){
    var elemento = document.getElementById("Correo").value;
    if( elemento === null || elemento.length === 0 || /^\s+$/.test(elemento) ) {
        alert('[ERROR] El campo debe tener algun valor');
        return false;
    }
    if( !(/\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)/.test(elemento)) ) {
        alert('[ERROR] El campo debe tener un email valido');
        return false;
        }

    return true;
}


function validaContraseña(){
    var elemento = document.getElementById("Contraseña").value;
    if( elemento === null || elemento.length === 0 || /^\s+$/.test(elemento) ) {
        alert('[ERROR] El campo debe tener algun valor');
        return false;
        }
    return true;
}


function validar(e) {
    if (validaNombre() && validaCedula() && validaCorreo() && validaContraseña() && confirm("Pulsa aceptar si deseas enviar la información")) {
        return true;
    } else {
        e.preventDefault();
        return false;
    }
}
