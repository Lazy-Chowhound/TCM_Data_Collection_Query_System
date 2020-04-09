$(function () {
    $("#searchBtn").click(function () {
        let content = $("#content").val();
        let option = $("#option option:selected").val();
        if (content === "")
            alert("请输入您想要搜索的内容");
        else
            window.location.href = "/index?opt=4&&prescriptionName=" + content + '&&page=1';
    });
    $("#backBtn").click(function () {
        window.history.go(-1);
    });
});