window.onload = iniciar; 

function iniciar() {
    document.getElementById("enviar").addEventListener('click', validar, false);
}

function validaUsuario(){
    var elemento = document.getElementById("username");
    if (!elemento.checkValidity()) {
        if (elemento.validity.valueMissing){
            alert('[ERROR] Debe introducir un nombre');
        }
        if(elemento.validity.patternMismatch){
            alert('[ERROR] El usuario debe tener entre 5 y 15 caracteres');
        }
        return false;
    }
    return true;
}

function validaContraseña(){
    var elemento = document.getElementById("password");
    if (!elemento.checkValidity()) {
        if (elemento.validity.valueMissing){
            alert('[ERROR] Debe introducir un password');
        }
        if(elemento.validity.patternMismatch){
            alert('[ERROR] El password debe tener minimo 5 caracteres');
        }
        return false;
    }
    return true;
}


function validar(e) {
    if (validaUsuario() && validaContraseña() && confirm("Pulsa aceptar si deseas enviar el formulario")) {
        return true;
    } else {
        e.preventDefault();
        return false;
    }
}


