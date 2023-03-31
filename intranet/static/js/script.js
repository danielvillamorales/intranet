function habilitar_boton(value = null) {
    var fechainicial = document.getElementById("id_fechainicial").value;
    var fechafinal = document.getElementById("id_fechafinal").value;
    var button = document.getElementById("button-agregar");
    var valor = false;
    console.log(fechafinal);
    console.log(fechainicial);
    

    if (value == 'inicial') {
        valor =  validar_horas(fechainicial);
        document.getElementById("id_fechafinal").disabled = !valor;
    } else if (value == 'final') {
        valor = validar_horas(fechafinal);
        document.getElementById("id_fechainicial").disabled = !valor;
    }

    if (valor == true) {
        if (new Date(fechainicial) >= new Date(fechafinal)) {
            console.log("la fecha inicial es mayor o igual a la fecha final");
            Swal.fire('!Error','la fecha inicial es mayor o igual a la fecha final','error')
            button.disabled = true;
        } else {
            console.log("la fecha inicial es menor a la fecha final");
            button.disabled = false;
        }
    }
};

function mostrar_foto(foto){
    console.log(foto);
    var imagen = document.getElementById("imgpromo_"+foto);
    if (imagen.style.display === "none") {
        imagen.style.display = "block";
      } else {
        imagen.style.display = "none";
      }

};

function validar_horas(fecha) {
    var button = document.getElementById("button-agregar");
    console.log(new Date(fecha).getHours());
    if (new Date(fecha).getHours() < 6    || new Date(fecha).getHours() > 20) {
        console.log("la hora es menor a 6 o mayor a 8 pm");
        Swal.fire('!Error','la hora es menor a 6 am o mayor a 8 pm no se encuentra dentro del horario de trabajo','error')
        button.disabled = true;
        return false;
    } else {
        console.log("la hora es mayor a 6 y menor a 8 pm");
        button.disabled = false;
        return true;
    }
}

function habilitar(value)
{
    if(value=="2")
    {
        // habilitamos
        document.getElementById("id_beneficio").disabled=false;
        document.getElementById("id_beneficio").style.display="inline";
        document.getElementById("pid_beneficio").style.display="inline";
    }else {
        // deshabilitamos
        document.getElementById("id_beneficio").disabled=true;
        document.getElementById("id_beneficio").style.display="none"
        document.getElementById("pid_beneficio").style.display="none"
    }
}


function confirmar(titulo, ruta){
    console.log(titulo);
    console.log(ruta);
    Swal.fire({
        title: 'Confirmacion',
        text: titulo,
        icon: 'question',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí',
        cancelButtonText: 'Cancelar'
      }).then((result) => {
        if (result.isConfirmed) {
          window.location.href = ruta;
        }
      });
}






