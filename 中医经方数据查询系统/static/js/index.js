$(function () {
    // 第一个按钮点击事件
    $(".prescription").click(function () {
        $("#loading").css("display", "flex");
        setTimeout(function () {
            $("#loading").css("display", "none");
        }, 1800);
    });

    //第二个按钮点击事件
    $(".medicine").click(function () {
        $("#loading").css("display", "flex");
        setTimeout(function () {
            $("#loading").css("display", "none");
        });
    });
});

function setTable() {
    document.getElementById('retrieve').style.display = 'none';
    document.getElementById('table').style.display = 'none';
    document.getElementById('reserve').style.display = 'none';
    setLoad();
    setTimeout(function () {
        document.getElementById('loading').style.display = 'none';
    }, 1800);
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.open("POST", "php/anonymous.php", true);
    xmlhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xmlhttp.send(null);
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
            var info = xmlhttp.responseText;
            var table = eval(info);
            var div = document.getElementById("table");
            var tab = "<table border='1' bordercolor='black' width='900' height='150' class='table2'>"
            tab += "<tr><th>编号</th><th>名称</th><th>状态</th><th>借出时间</th><th>应还时间</th><th>是否预约</th></tr>"
            for (var i = 0; i < table.length; i++) {
                tab += "<tr>";
                for (var j = 0; j < 5; j++) {
                    if (table[i][j]) {
                        tab += "<td>" + table[i][j] + "</td>";
                    } else {
                        tab += "<td></td>"
                    }
                }
                if (table[i][2] == "可借")
                    tab += "<td><button  class='button reservebtn' name='reservebtn' onclick='directReserve(this)'>预约</button></td>"
                else
                    tab += "<td><button  class='unreservebtn' name='reservebtn' onclick='directReserve(this)'>不可预约</button></td>"
                tab += "</tr>";
            }
            tab += "</table>"
            div.innerHTML = tab;
            var button = document.getElementsByName('reservebtn')
            for (var id = 0; id < button.length; id++) {
                button[id].id = '' + id;
            }
            document.getElementById('table').style.display = 'block';
        }
    }
}

function directReserve(button) {
    var id = button.id;
    var table = document.getElementsByTagName('td');
    var number = table[id * 6].innerHTML;
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.open('POST', 'php/directReserve.php', true);
    xmlhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xmlhttp.send('number=' + number);
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.status == 200 && xmlhttp.readyState == 4) {
            var info = xmlhttp.responseText;
            var result = eval(info);
            if (result == 'success') {
                alert("预约成功!");
            } else {
                alert("预约失败!");
            }
        }
    }
}

// 第二个按钮触发事件
function setSearch() {
    document.getElementById('table').style.display = 'none';
    document.getElementById('retrieve').style.display = 'block';
    document.getElementById('reserve').style.display = 'none';
    document.getElementById('bookname').value = '';
    document.getElementById('hide').style.display = 'none';
}

function search() {
    if (document.getElementById('videoname').value == "") {
        alert("请输入名称！");
    } else {
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.open('POST', 'php/search.php', true)
        xmlhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xmlhttp.send('name=' + document.getElementById('videoname').value);
        xmlhttp.onreadystatechange = function () {
            if (xmlhttp.status === 200 && xmlhttp.readyState == 4) {
                var info = xmlhttp.responseText;
                var table = eval(info);
                var div = document.getElementById('searchresult');
                if (table == 'none') {
                    var tab = "<table border='1' bordercolor='black' width='900' height='150' id='hide' class='none'>";
                    tab += "<tr><th>暂无相关影像制品信息</th></tr>";
                    div.innerHTML = tab;
                } else {
                    var tab = "<table border='1' bordercolor='black' width='900' height='150' id='hide' class='searchresult'>";
                    tab += "<tr><th>编号</th><th>名称</th><th>状态</th><th>借出时间</th><th>应还时间</th></tr>";
                    for (var i = 0; i < table.length; i++) {
                        tab += "<tr>";
                        for (var j = 0; j < 5; j++) {
                            if (table[i][j]) {
                                tab += "<td>" + table[i][j] + "</td>";
                            } else {
                                tab += "<td></td>"
                            }
                        }
                        tab += "</tr>";
                    }
                    tab += "</table>"
                    div.innerHTML = tab;
                }
            }
        }
    }
}

function setReserve() {
    document.getElementById('table').style.display = 'none';
    document.getElementById('retrieve').style.display = 'none';
    document.getElementById('reserve').style.display = 'block';
    document.getElementById('videoname').value = '';
    document.getElementById('hide').style.display = 'none';
    document.getElementById('reservebutton').style.display = 'none';
    document.getElementById('name').value = '';
}

function reserve() {
    if (document.getElementById('name').value == "") {
        alert("请输入名称！");
    } else {
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.open('POST', 'php/search.php', true)
        xmlhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xmlhttp.send('name=' + document.getElementById('name').value);
        xmlhttp.onreadystatechange = function () {
            if (xmlhttp.status == 200 && xmlhttp.readyState == 4) {
                var info = xmlhttp.responseText;
                var table = eval(info);
                var div = document.getElementById('reserveresult');
                if (table == 'none') {
                    var tab = "<table border='1' bordercolor='black' width='900' height='150' id='hide' class='none'>";
                    tab += "<tr><th>暂无相关影像制品信息</th></tr>";
                    div.innerHTML = tab;
                } else {
                    var tab = "<table border='1' bordercolor='black' width='900' height='150' id='hide' class='searchresult'>";
                    tab += "<tr><th>编号</th><th>名称</th><th>状态</th><th>借出时间</th><th>应还时间</th></tr>";
                    for (var i = 0; i < table.length; i++) {
                        tab += "<tr>";
                        for (var j = 0; j < 5; j++) {
                            if (table[i][j]) {
                                tab += "<td>" + table[i][j] + "</td>";
                            } else {
                                tab += "<td></td>"
                            }
                        }
                        tab += "</tr>";
                    }
                    tab += "</table>"
                    div.innerHTML = tab;
                    document.getElementById('reservebutton').style.display = 'block';
                }
            }
        }
    }
}

function reservevideo() {
    var name = document.getElementById('name').value;
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.open('POST', 'php/reserve.php', true);
    xmlhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xmlhttp.send("name=" + name);
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.status == 200 && xmlhttp.readyState == 4) {
            var info = xmlhttp.responseText;
            var result = eval(info);
            if (result == 'success') {
                alert('预约成功！');
            } else if (result == 'failure') {
                alert('该制品已借出!');
            }
        }
    }
}



