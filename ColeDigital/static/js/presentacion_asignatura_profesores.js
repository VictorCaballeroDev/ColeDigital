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

$(document).ready(function() {

    let tareaID =""
    $('.eliminar-tarea-btn').click(function() {
        tareaID = $(this).data('bs-id')
    });

    $('#confirmar-eliminacion').click(function() {
        $.ajax({
            type: 'POST',
            url: '/eliminar_tarea/',
            data: {
                'id_tarea': tareaID,
                'csrfmiddlewaretoken': csrftoken
            },
            success: function(data) {
                location.reload()
                $('#tareas-tab').attr('aria-selected', 'true')
            }
        })
    });
});