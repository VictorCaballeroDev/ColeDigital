function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken')

/*
function eliminarAsignatura(id_asignatura) {
    if(confirm('Esta acción eliminará la asignatura y todo su contenido ¿desea continuar?')) {

        $.ajax({
            type: 'POST',
            url: '/eliminar_asignatura/',
            data: {
                'id_asignatura': id_asignatura,
                'csrfmiddlewaretoken': csrftoken
            },
            success: function(data) {
                location.reload()
            }
        })
    }
}
*/


$(document).ready(function() {

    let asignaturaNombre = ""
    let asignaturaId =""

    $('.eliminar-asignatura-btn').click(function() {
        asignaturaId = $(this).data('bs-id')
        asignaturaNombre = $(this).data('nombre')
    });

    $('#confirmar-eliminacion').click(function() {
        $.ajax({
            type: 'POST',
            url: '/eliminar_asignatura/',
            data: {
                'id_asignatura': asignaturaId,
                'csrfmiddlewaretoken': csrftoken
            },
            success: function(data) {
                location.reload()
            }
        })
    });

    
    $('.cambiar-nombre-btn').click(function() {
        const asignaturaId = $(this).data('bs-id')
        asignaturaNombre = $(this).data('bs-nombre')
        $('#id_asignatura_id').val(asignaturaId)
        $('#id_nombre').val(asignaturaNombre)
        $('#error-message').hide()
    });

    $('#cambiar-nombre-form').submit(function(event) {
        const inputAsignaturaNombreValor = $('#id_nombre').val()
        if (inputAsignaturaNombreValor === asignaturaNombre) {
            $('#error-message').show();
            event.preventDefault();
        }
    });

});