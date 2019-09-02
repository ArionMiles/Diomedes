$(document).ready(function () {
    $.ajax({
        url: "/ajax/movies",
        type: "get",
        async: true,
        cache: true,
        success: function (data) {
            $("#id_name").autocomplete({
                source: data.movies
            });
        }
    });
});