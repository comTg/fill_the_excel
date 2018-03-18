function td_click() {
    var td = $(this);
    var text = td.text();
    var input = $("<textarea></textarea>");
    td.html("");
    input.text(text);

    function put_valueto_td(node) {
        //获取当前文本框的内容
        var inputext = node.val().trim();
        //清空td里边的内容,然后将内容填充到里边
        var tdNode = node.parent();
        tdNode.html(inputext);
        //让td重新拥有点击事件
        tdNode.click(td_click);
    }

    //4.5让文本框可以相应键盘按下的事件
    input.keyup(function (event) {
        //记牌器当前用户按下的键值
        var myEvent = event || window.event;//获取不同浏览器中的event对象
        var kcode = myEvent.keyCode;
        //判断是否是回车键按下
        if (kcode == 13) {
            put_valueto_td(input);
        }
    }).blur(function () {
        put_valueto_td(input);
    });
    //5，把文本框加入到td里边去
    td.append(input);
    // 增加textarea自增高功能
    $("textarea").autogrow();
    //5.5让文本框里边的文章被高亮选中
    //需要将jquery的对象转换成dom对象
    var inputdom = input.get(0);
    inputdom.select();
    //6,需要清楚td上的点击事件
    td.unbind("click");
}

function set_table(title) {
    $.get("/api/getexcel", {title: title}, function (data, status) {
            var title_node = $("#show_table caption");
            var head_tr_node = $("#show_table thead tr");
            var tbody_node = $("#show_table tbody");
            title_node.empty();
            head_tr_node.empty();
            tbody_node.empty();
            if (data != "null") {
                var result = $.parseJSON(data);
                $.each(result, function (position, value) {
                    var tr_node = $("<tr></tr>");
                    for (var key in value) {
                        if (position == 0) {
                            title_node.text(title);
                            var head_th_node = $("<th></th>").text(key);
                            head_tr_node.append(head_th_node);
                        }
                        var td_node = $("<td></td>").addClass("text-info").text(value[key]);
                        tr_node.append(td_node);
                    }
                    tbody_node.append(tr_node);
                });
                var tds = $("td").not(":first-child");
                // var serial_td = $("td:first-child");
                // serial_td.click(delete_row);
                tds.click(td_click);
            }
        }
    );

}

// 提交表格中修改的内容
function submit_change() {
    var result = {};
    // p:position i:item
    $("tbody>tr").each(function (p, i) {
        var this_td = {}
        var tds = $(this).children();
        tds.each(function (p, i) {
            this_td[p] = $(this).text();
        });
        result[p] = this_td;
    });
    result = JSON.stringify(result);
    var title = $("table>caption").text();
    $.post("/api/change/", {
        "data": result,
        "title": title,
        'csrfmiddlewaretoken': '{% csrf_token %}'
    }, function (data, status) {
        if(data=="ok"){
            alert("修改表单成功!");
        }else{
            alert("修改表单失败!");
        }
    });
}

// 双击序号删除该列
function delete_row(){
    var td = $(this);
    console.log(td.text());
}

var init = function () {
    $.get("/api/gettitle", function (data, status) {
            if (data != "null") {
                var result = $.parseJSON(data);
                const list_group = $(".list-group");
                $.each(result, function (name, value) {
                    var node = $('<button></button>').addClass("btn btn-info list-group-item").text(value);
                    list_group.append(node);
                });
                $("button.list-group-item").click(function () {
                    var title = $(this).text();
                    set_table(title);
                });
                var first_title = $(".list-group button:first").text();
                set_table(first_title);
            }

        }
    );
    $("#submit").click(function () {
        var r = confirm("是否确认提交修改?");
        if (r == true) {
            submit_change();
        }
    });
};