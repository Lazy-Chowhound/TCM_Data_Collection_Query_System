$(function () {
    $("#searchBtn").click(function () {
        let content = $("#content").val();
        let option = $("input:radio[name='option']:checked").val();
        if (content === "")
            alert("请输入您想要搜索的内容");
        else if (option == null) {
            alert("请选择选项");
        } else {
            if (option === 'illness') {
                window.location.href = 'index?' + 'opt=1' + '&&illness=' + content + '&&page=1';
            } else if (option === "symptom") {
                window.location.href = 'index?' + 'opt=2' + '&&symptom=' + content + '&&page=1';
            } else if (option === "herb") {
                window.location.href = 'index?' + 'opt=3' + '&&herb=' + content + '&&page=1';
            } else if (option === "prescription") {
                window.location.href = 'index?' + 'opt=4' + '&&prescriptionName=' + content + '&&page=1';
            }
        }
    });
});