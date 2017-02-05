function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function loadTracks(data = 1) {
    $.ajax({
        url: "/track_list/",
        data: { "page": data }
    }).done(function(data) {
        $('#siteloader').empty();
        $('#siteloader').html(data);
        $('input.rating').rating();
        $('[data-toggle="tooltip"]').tooltip()
        $('#loading').hide();
        toastr.info("Tracks loaded")

    }).fail(function(jqXHR, textStatus) {
        toastr.error(JSON.parse(jqXHR['responseText'])['message'])
    });
}

function loadGenres(data = 1) {
    $.ajax({
        url: "/genre/",
        data: { "page": data }
    }).done(function(data) {
        $('#siteloader').empty();
        $('#siteloader').html(data);
        $('input.rating').rating();
        $('[data-toggle="tooltip"]').tooltip()
        $('#loading').hide();
        toastr.info("Genres loaded")
    }).fail(function(jqXHR, textStatus) {
        toastr.error(JSON.parse(jqXHR['responseText'])['message'])
    });
}

$(document).on('click', 'span.track-paginate', function() {
    $('#loading').show();
    $('#siteloader').empty();
    loadTracks($(this).data('href'));
});

$(document).on('click', 'span.genre-paginate', function() {
    $('#loading').show();
    $('#siteloader').empty();
    loadGenres($(this).data('href'));
});

$(document).on('click', "ul.nav.nav-pills li", function() {
    if (!$(this).hasClass("active")) {
        $("ul.nav.nav-pills li").each(function() {
            $(this).toggleClass("active");
        });
        $("button.genre_track_btn").each(function() {
            $(this).toggleClass("hidden");
            $(this).toggleClass("invisible");
            $(this).toggleClass("show");
        });
    }
    $('#trackSearch').val('')
    $('#loading').show();
    $('#siteloader').empty();
    if ($(this).hasClass('genre')) {
        loadGenres();
    } else {
        loadTracks();
    }
});

$(document).on('keyup', '#trackSearch', function() {
    var query = $('#trackSearch').val();
    if (!query) {
        $('ul.nav.nav-pills li.track').click();
    } else {
        $('#loading').show();
        $('#siteloader').empty();
        $.ajax({
            url: "search?query=" + query,
        }).done(function(data) {
            $('#siteloader').empty().html(data['responseText'])
            $('input.rating').rating();
            $('#loading').hide();
        }).fail(function(jqXHR, textStatus) {
            toastr.error(JSON.parse(jqXHR['responseText'])['message'])
        });
    }
});

$('button.search-button').on('click', function() {
    var query = $('#trackSearch').val();
    if (!query) {
        $('ul.nav.nav-pills li.track').click();
    } else {
        $('#loading').show();
        $('#siteloader').empty();
        $.ajax({
            url: "search?query=" + query,
        }).done(function(data) {
            $('#siteloader').empty().html(data['responseText'])
            $('input.rating').rating();
            $('#loading').hide();
        }).fail(function(jqXHR, textStatus) {
            toastr.error(JSON.parse(jqXHR['responseText'])['message'])
        });
    }
});

$('#tracks_modal').on('show.bs.modal', function(event) {
    $("select#track-genre").prop('selectedIndex', -1);
    var modal = $(this)
    $(this).find('input.form-control').val('')
    var button = $(event.relatedTarget)
    var recipient = button.data('track-id')
    if (button.hasClass('track-edit-btn')) {
        $.ajax({
            url: "/" + recipient + "/"
        }).done(function(data) {
            modal.find('#track-id').val(data['track_id']).attr('value', data['track_id'])
            modal.find('#track-title').val(data['title']).attr('value', data['title'])
            modal.find('#track-rating').val(data['rating']).attr('value', data['rating'])
            jQuery.each(data['genre'], function(index, item) {
                $('select#track-genre option[value=' + item["genre_id"] + ']').prop("selected", "selected");
            });
            $('select#track-genre').attr('value', $('select#track-genre').val());
        }).fail(function(jqXHR, textStatus) {
            toastr.error(JSON.parse(jqXHR['responseText'])['message'])
        });
    }
})

$('#genres_modal').on('show.bs.modal', function(event) {
    var modal = $(this)
    $(this).find('input.form-control').val('')
    var button = $(event.relatedTarget)
    var recipient = button.data('genre-id')
    if (button.hasClass('genre-edit-btn')) {
        $.ajax({
            url: "/genre/" + recipient + "/"
        }).done(function(data) {
            modal.find('#genre-id').val(data['genre_id']).attr('value', data['genre_id'])
            modal.find('#genre-label').val(data['title']).attr('value', data['title'])
        }).fail(function(jqXHR, textStatus) {
            toastr.error(JSON.parse(jqXHR['responseText'])['message'])
        });
    }
})

$("form.tracks").submit(function(e) {
    var form = $(this);
    var ajax_url = '';
    data = {
        track_title: $('#track-title').val(),
        track_rating: $('#track-rating').val(),
    }
    if ($('#track-id').val() != 0) {
        data['track_id'] = $('#track-id').val(),
            ajax_url = '/' + $('#track-id').val() + '/edit';
    } else {
        ajax_url = '/add';
    }

    var track_genre = []
    if ($('select#track-genre').val() != null) {
        track_genre = $('select#track-genre option:selected').map(function() {
            return { value: this.text, id: this.value }
        }).get()
    }

    data['track_genre'] = track_genre;

    csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $.ajax({
        url: ajax_url,
        type: 'POST',
        data: JSON.stringify(data), // data to be submitted
    }).done(function(data) {
        $("#tracks_modal").modal('toggle');
        if ($('#track-id').val() != 0) {
            toastr.success("The track has been successfully changed")
        } else {
            toastr.success("Track successfully added");
        }
    }).fail(function(jqXHR, textStatus) {
        toastr.error(JSON.parse(jqXHR['responseText'])['message'])
    });
    return false;
});

$("form.genres").submit(function(e) {
    var form = $(this);
    var ajax_url = '';
    data = {
        genre_type: $('#genre-label').val(),
    }
    if ($('#genre-id').val() != 0) {
        data['genre_id'] = $('#genre-id').val();
        JSON.stringify(data);
        ajax_url = '/genre/' + $('#genre-id').val() + '/edit';
    } else {
        ajax_url = '/genre/add';
    }
    csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $.ajax({
        url: ajax_url,
        type: 'POST',
        data: data, // data to be submitted
    }).done(function(data) {
        $("#genres_modal").modal('toggle');
        if ($('#genre-id').val() != 0) {
            toastr.success("The genre has been successfully changed")
        } else {
            toastr.success("Genre successfully added");
        }
    }).fail(function(jqXHR, textStatus) {
        toastr.error(JSON.parse(jqXHR['responseText'])['message'])
    });
    return false;
});

$(function() {
    $('input.rating').rating();
    loadTracks();
    $('[data-toggle="tooltip"]').tooltip()
});
