window.onload = iniciar; 

function iniciar() {
    document.getElementById("Actualizar").addEventListener('click', validar, false);
    document.getElementById("Eliminar").addEventListener('click', validar, false);
}

function validaNombre(){
    var elemento = document.getElementById("Nombre").value;
    if( elemento === null || elemento.length === 0 || /^\s+$/.test(elemento) ) {
        alert('[ERROR] El campo Nombre debe tener algun valor');
        return false;
        }    
    return true;
}

function validaCedula(){
    var elemento = document.getElementById("Cedula").value;
    if( elemento === null || elemento.length === 0 || /^\s+$/.test(elemento) ) {
        alert('[ERROR] El campo Cedula debe tener algun valor');
        return false;
    }
    else if(isNaN(elemento)){
        alert('[ERROR] El campo Cedula debe tener valores numericos');
        return false; 
    }
    return true;
}

function validaCorreo(){
    var elemento = document.getElementById("Correo").value;
    if( elemento === null || elemento.length === 0 || /^\s+$/.test(elemento) ) {
        alert('[ERROR] El campo Correo debe tener algun valor');
        return false;
        } 
    else if( !(/\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)/.test(elemento)) ) {
        alert('[ERROR] El campo Correo debe tener un email valido');
        return false;
        }
    return true;
}

function validaContraseña(){
    var elemento = document.getElementById("Precio").value;
    if( elemento === null || elemento.length === 0 || /^\s+$/.test(elemento) ) {
        alert('[ERROR] El campo Contraseña debe tener algun valor');
        return false;
        } 
    else if(isNaN(elemento)){
        alert('[ERROR] El campo Contraseña debe tener valores numericos');
        return false;
    }
    return true;
}

function validar(e) {
    if (validaNombre() && validaCedula() && validaCorreo() && validaContraseña() && confirm("Pulsa aceptar si deseas enviar la informacion")) {
        return true;
    } else {
        e.preventDefault();
        return false;
    }
}