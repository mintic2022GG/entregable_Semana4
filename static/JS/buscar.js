productos = [
    {nombre: 'tinto', valor: 1000},
    {nombre: 'pan rollo', valor: 500},
    {nombre: 'tamal', valor: 8000},
    {nombre: 'leche', valor: 3000},
    {nombre: 'huevo', valor: 500},
    {nombre: 'perico', valor: 2000},
    
    
]

busqueda = document.querySelector('#busqueda');
resultado = document.querySelector('#resultado');

filtrar = ()=>{
    resultado.innerHTML = '';
   texto = busqueda.value.toLowerCase();
    for(let producto of productos){
        let nombre = producto.nombre.toLowerCase();
        if (nombre.indexOf(texto) !== -1){
            resultado.innerHTML += `
            <li>${producto.nombre} - valor: ${producto.valor}</li>`;
        }else{
            resultado.innerHTML;
        }
    }
        if(resultado.innerHTML === ''){
          resultado.innerHTML += `
            <li>Producto no encontrado...</li>`;  
        }
}

busqueda.addEventListener('keyup',filtrar);
