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

    let estudianteId =""
    $('.eliminar-estudiante-btn').click(function() {
        estudianteId = $(this).data('bs-id')
    });

    $('#confirmar-eliminacion').click(function() {
        $.ajax({
            type: 'POST',
            url: '/eliminar_estudiante/',
            data: {
                'id_estudiante': estudianteId,
                'csrfmiddlewaretoken': csrftoken
            },
            success: function(data) {
                location.reload()
            }
        })
    });
});