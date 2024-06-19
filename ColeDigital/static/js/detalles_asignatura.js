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

function desapuntarProfesor(id_profesor) {
    if(confirm('Esta acción desapuntará al profesor de la asignatura, ¿desea continuar?')) {

        $.ajax({
            type: 'POST',
            url: '/desapuntar_profesor/',
            data: {
                'id_profesor': id_profesor,
                'id_asignatura': id_asignatura,
                'csrfmiddlewaretoken': csrftoken
            },
            success: function(data) {
                location.reload()
            }
        })
    }
}

function desapuntarEstudiante(id_estudiante) {
    if(confirm('Esta acción desapuntará al estudiante de la asignatura, ¿desea continuar?')) {

        $.ajax({
            type: 'POST',
            url: '/desapuntar_estudiante/',
            data: {
                'id_estudiante': id_estudiante,
                'id_asignatura': id_asignatura,
                'csrfmiddlewaretoken': csrftoken
            },
            success: function(data) {
                location.reload()
            }
        })
    }
}



$(document).ready(function() {

    let id_profesor = ""

    $('.desapuntar-profesor-btn').click(function() {
        id_profesor = $(this).data('bs-idprofesor')
    })


    $('#confirmar-desapuntar').click(function() {
        $.ajax({
            type: 'POST',
            url: '/desapuntar_profesor/',
            data: {
                'id_profesor': id_profesor,
                'id_asignatura': id_asignatura,
                'csrfmiddlewaretoken': csrftoken
            },
            success: function(data) {
                location.reload()
            }
        })
    });
})