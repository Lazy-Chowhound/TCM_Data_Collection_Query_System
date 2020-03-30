$(function () {
    $("#search_button").click(function () {
        let content = $("#content").val();
        let option = $("input:radio[name='option']:checked").val();
        if (content === "")
            alert("请输入您想要搜索的内容");
        else if (option == null) {
            alert("请选择选项");
        } else {
            if (option === 'illness') {
                window.location.href = 'index?' + 'opt=1' + '&&illness=' + content;
            } else if (option === "symptom") {
                window.location.href = 'index?' + 'opt=2' + '&&symptom=' + content;
            } else if (option === "herb") {
                window.location.href = 'index?' + 'opt=3' + '&&herb=' + content;
            } else if (option === "record") {
                window.location.href = 'index?' + 'opt=4' + '&&record=' + content;
            }
            // $.ajax({
            //     type: "POST",
            //     // 发送的数据格式
            //     contentType: 'application/json',
            //     // 期待后端返回的格式
            //     dataType: "json",
            //     url: '/display',
            //     data: JSON.stringify({'content': content, 'option': option}),
            //     success: function (res) {
            //         let option = res.option;
            //         if (option === '-1') {
            //             alert('查询失败，请重试！');
            //         } else if (option === '3') {
            //             window.location.href = 'index?' + 'opt=' + res.option + '&&herb=' + res.name + '&&effect:' + res.effect;
            //         }
            //     },
            //     error: function (e) {
            //         alert("网络出错");
            //     }
            // })
        }
    });
});