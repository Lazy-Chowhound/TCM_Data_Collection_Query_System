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