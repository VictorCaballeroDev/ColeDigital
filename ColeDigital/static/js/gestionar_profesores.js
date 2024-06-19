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

    let profesorId =""
    $('.eliminar-profesor-btn').click(function() {
        profesorId = $(this).data('bs-id')
    });

    $('#confirmar-eliminacion').click(function() {
        $.ajax({
            type: 'POST',
            url: '/eliminar_profesor/',
            data: {
                'id_profesor': profesorId,
                'csrfmiddlewaretoken': csrftoken
            },
            success: function(data) {
                location.reload()
            }
        })
    });
});