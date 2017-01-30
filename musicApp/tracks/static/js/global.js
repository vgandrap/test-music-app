function loadTracks(data = 1) {
    $.get("/track_list/", { "page": data }).done(function(data) {
        $('#siteloader').html(data);
        $('input.rating').rating();
    $('[data-toggle="tooltip"]').tooltip()
    });
}

function loadGenres(data = 1) {
    $.get("/genre/", { "page": data }).done(function(data) {
        $('#siteloader').html(data);
        $('input.rating').rating();
    $('[data-toggle="tooltip"]').tooltip()
    });
}

$(document).on('click', 'span.track-paginate', function() {
    $('#siteloader').empty();
    loadTracks($(this).data('href'));
});

$(document).on('click', 'span.genre-paginate', function() {
    $('#siteloader').empty();
    loadGenres($(this).data('href'));
});

// $("ul.nav.nav-pills li").each(function() {
$(document).on('click', "ul.nav.nav-pills li", function() {
    $("ul.nav.nav-pills li").each(function() {
        $(this).toggleClass("active");
    });
    $("button.genre_track_btn").each(function() {
        $(this).toggleClass("hidden");
        $(this).toggleClass("invisible");
        $(this).toggleClass("show");
    });
    $('#siteloader').empty();
    if ($(this).hasClass('genre')) {
        loadGenres();
    } else {
        loadTracks();
    }
});
// });

$(function() {

    // Toggle Navbar Active Links
    // $("ul.nav.navbar-nav li").each(function() {
    //     $(this).on('click', function() {
    //         $("ul.nav.navbar-nav li").each(function() {
    //             $(this).removeClass("active");
    //         });
    //         $(this).addClass("active");
    //     });
    // });


    $('input.rating').rating();

    loadTracks();
    $('[data-toggle="tooltip"]').tooltip()
});
