$(function () {
    let height = $('.recordArea').height() + $('.top').height() + 100;
    if (height > $(window).height())
        $("html").css("height", height + "px");

    let arr = $(".recordArea p");
    for (let i = 0; i < arr.length; i++) {
        if (arr.eq(i).text().substring(2, 3) === '诊' && arr.eq(i).text().substring(0, 1) === '【') {
            arr.eq(i).addClass('subtitle');
        }
    }
});