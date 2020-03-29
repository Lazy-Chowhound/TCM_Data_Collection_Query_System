$(function () {
    $("#search_button").click(function () {
        const symptom = $("#content").val();
        if (symptom === "")
            alert("请输入");
        else {
            $.ajax({
                type: "POST",
                // 发送的数据格式
                contentType: 'application/json',
                // 期待后端返回的格式
                dataType: "json",
                url: '/display',
                data: JSON.stringify({'symptom': symptom}),
                success: function (res) {
                    window.location.href = 'index?' + 'sym=' + res.symptom;
                },
                error: function (e) {

                }
            })
        }
    });
});