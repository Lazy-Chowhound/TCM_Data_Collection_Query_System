$(function () {
    $("#record").click(function () {
        $('#record').addClass('clickbtn');
        $('#herb').removeClass('clickbtn');
        $('#prescription').removeClass('clickbtn');
        window.location.href="/index?"+ 'opt=1';
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