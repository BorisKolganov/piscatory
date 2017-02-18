/**
 * Created by Boris on 18.02.17.
 */
$(document).ready(function () {
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie != '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) == (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }

            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });
        $('.delete-form').submit(function (event) {
        var action = $(this).attr('action');
        event.preventDefault();
        swal({
            title: 'Вы уверены?',
            text: "Удаление отменить невозможно",
            type: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Да, удалить',
            cancelButtonText: 'Отменить',
            confirmButtonClass: 'btn btn-success btn-space',
            cancelButtonClass: 'btn btn-danger',
            buttonsStyling: false,
            showLoaderOnConfirm: true,
            preConfirm: function () {
                return new Promise(function (resolve, reject) {
                    $.post(action).done(function (data) {
                        resolve(data)
                    }).fail(function () {
                        reject('Удаление невозможно')
                    })
                })
            }
        }).then(function (data) {
            swal({
                type: 'success',
                title: 'Удаление прошло успешно',
                confirmButtonText: 'Ок',
                confirmButtonClass: 'btn btn-success btn-space',
                allowOutsideClick: false
            }).then(function () {
                if (data.redirect_url)
                    window.location = data.redirect_url;
                window.location = '/'
            });

        });

    })
});