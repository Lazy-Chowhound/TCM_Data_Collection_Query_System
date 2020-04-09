$(function () {
    $("#searchBtn").click(function () {
        let content = $("#content").val();
        if (content === "")
            alert("请输入您想要搜索的内容")
        else {
            window.location.href = "/index?opt=3&&herb=" + content + '&&page=1';
        }
    });
});