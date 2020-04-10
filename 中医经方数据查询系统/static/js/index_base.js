$(function () {
    $("#record").click(function () {
        let opt = getOpt();
        if (opt !== '1' || opt !== '2')
            window.location.href = "/index?" + 'opt=1';
    });
    $("#herb").click(function () {
        let opt = getOpt();
        if (opt !== '3')
            window.location.href = "/index?" + 'opt=3';
    });
    $("#prescription").click(function () {
        let opt = getOpt();
        if (opt !== '4')
            window.location.href = "/index?" + 'opt=4';
    });
});

function getOpt() {
    let url = window.location.search;
    let str = url.substring(url.indexOf("?") + 1);
    let arr = str.split("&");
    for (let i = 0; i < arr.length; i++) {
        if (arr[i].search("opt") !== -1) {
            return arr[i].substring(arr[i].indexOf("=") + 1);
        }
    }
}

function getParameter() {
    let len = arguments.length;
    let url = window.location.search;
    let parameter = url.substring(url.indexOf("?") + 1);
    let mainUrl = url.substring(0, url.indexOf("?"));
    let arr = parameter.split("&");
    let res = [];
    for (let i = 0; i < len; i++) {
        for (let j = 0; j < arr.length; j++) {
            if (arr[j].search(arguments[i]) !== -1) {
                res.push(arr[j].substring(arr[j].indexOf("=") + 1));
            }
        }
    }
    res.push(mainUrl);
    return res;
}

function showPrompt() {
    $(".main").fadeIn();
    $('.promptBox').delay(300).slideDown();
    $('.prompt_cancel').click(function () {
        $('.promptBox').fadeOut();
    });
}