$(function () {
    $("#index").click(function () {
        window.location.href = "/search";
    });
    $("#back").click(function () {
        history.go(-1);
    });
});