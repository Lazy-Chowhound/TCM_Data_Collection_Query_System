$(function () {
    $("#record").click(function () {
        $('#record').addClass('clickbtn');
        $('#herb').removeClass('clickbtn');
        $('#prescription').removeClass('clickbtn');
    });
    $("#herb").click(function () {
        $('#herb').addClass('clickbtn');
        $('#record').removeClass('clickbtn');
        $('#prescription').removeClass('clickbtn');
    });
    $("#prescription").click(function () {
        $('#prescription').addClass('clickbtn');
        $('#record').removeClass('clickbtn');
        $('#herb').removeClass('clickbtn');
    });
});