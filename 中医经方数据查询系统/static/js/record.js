$(function () {
    $("#searchBtn").click(function () {
        let content = $("#content").val();
        let option = $("#option option:selected").val();
        if (content === "")
            alert("请输入您想要搜索的内容");
        else {
            if (option === 'illness')
                window.location.href = '/index?opt=1&&illness=' + content;
            else
                window.location.href = '/index?opt=2&&symptom=' + content;
        }
    });
});

