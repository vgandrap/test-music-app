$(document).ready(function() {

    // Toggle Navbar Active Links
    // $("ul.nav.navbar-nav li").each(function() {
    //     $(this).on('click', function() {
    //         $("ul.nav.navbar-nav li").each(function() {
    //             $(this).removeClass("active");
    //         });
    //         $(this).addClass("active");
    //     });
    // });

    $("ul.nav.nav-pills li").each(function() {
        $(this).on('click', function() {
            $("ul.nav.nav-pills li").each(function() {
                $(this).removeClass("active");
            });
            $(this).addClass("active");
        });
    });

    $('input.rating').rating();

});
