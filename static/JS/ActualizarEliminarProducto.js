window.onload = iniciar; 

function iniciar() {
    document.getElementById("Actualizar").addEventListener('click', validar, false);
    document.getElementById("Eliminar").addEventListener('click', validar, false);
}

function validaNombre(){
    var elemento = document.getElementById("Nombre").value;
    if( elemento === null || elemento.length === 0 || /^\s+$/.test(elemento) ) {
        alert('[ERROR] El campo debe tener algun valor');
        return false;
        }    
    return true;
}

function validaReferencia(){
    var elemento = document.getElementById("Referencia").value;
    if( elemento === null || elemento.length === 0 || /^\s+$/.test(elemento) ) {
        alert('[ERROR] El campo debe tener algun valor');
        return false;
        }    
    return true;
}

function validaCantidad(){
    var elemento = document.getElementById("Cantidad").value;
    if( elemento === null || elemento.length === 0 || /^\s+$/.test(elemento) ) {
        alert('[ERROR] El campo debe tener algun valor');
        return false;
        } 
    else if(isNaN(elemento)){
        alert('[ERROR] El campo debe tener valores numericos');
        return false;
    }
    return true;
}

function validaPrecio(){
    var elemento = document.getElementById("Precio").value;
    if( elemento === null || elemento.length === 0 || /^\s+$/.test(elemento) ) {
        alert('[ERROR] El campo debe tener algun valor');
        return false;
        } 
    else if(isNaN(elemento)){
        alert('[ERROR] El campo debe tener valores numericos');
        return false;
    }
    return true;
}

function validar(e) {
    if (validaNombre() && validaReferencia() && validaCantidad() && validaPrecio() && confirm("Pulsa aceptar si deseas enviar la informacion")) {
        return true;
    } else {
        e.preventDefault();
        return false;
    }
}