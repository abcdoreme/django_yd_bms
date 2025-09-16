$(document).ready(function () {
    $("#usersdetails").click(function () {
        $.ajax({
            type: "POST",
            dataType: "json",
            url: "/userLogin/capitalDetails",
            data: $("#usersDetailsOrder").serialize(),
            success: function (result) {
                if(result=="账号信息异常！")
                {
                    getDetails({}, "tabDetails");
                }
                else
                {
                    getDetails(result, "tabDetails");           
                }
                alert("查询成功!");
            },
            error: function () {
                alert("由于系统原因查询失败!");
            }
        });
    });
});

function getDetails (json, eleId) {
    //默认的每页最多记录数
    var num1 = 10;
    //每页真实的记录数
    var num2;
    //默认展示第一页
    var page = 1;
 
    //切换前后页面和页码的按钮
    var prev = document.getElementById("prev");
    var pages = document.getElementById("pages");
    var next = document.getElementById("next");
    prev.innerHTML = "《";
    next.innerHTML = "》";
 
    //计算总页数
    var count = Object.keys(json).length;
    //生成页码按钮
    function creatPages(){
        pages.innerHTML = "";
        for(var i = 0; i < Math.ceil(count / 10); i++){
            pages.innerHTML += `<button json-page="${i+1}">\xa0${i+1}\xa0</button>`;
            //pages.innerHTML += " <button json-page='${i+1}'>"+(i+1)+" <button>";
        }
    }
    creatPages();
    
    //渲染每一页的数据内容
    function renderPage(){
        //设置表头
        var str = "<tr><th>序号</th><th>交易时间</th><th>交易金额</th><th>交易币种</th><th>交易明细</th></tr>"
        document.getElementById(eleId).innerHTML = str;
 
        //判断当前选择的页码对应的记录数
        if(count - num1 * (page - 1) >= 10){
            num2 = 10;
        }
        else{
            num2 = count - num1 * (page - 1);
        }
 
        //渲染该页对应的数据
        var str1 = "";
        for(var i = num1 * (page - 1); i < num2 + num1 * (page - 1); i++){
            str1 += "<tr>";
            str1 += "<td>" + (parseInt(i)+1) + "</td>";
            str1 += "<td>" + json[i].iotime + "</td>";
            str1 += "<td>" + json[i].ioamount + "</td>";
            str1 += "<td>" + json[i].moneytype + "</td>";
            str1 += "<td>" + json[i].iodescription + "</td>";
            str1 += "</tr>";
        }
        document.getElementById(eleId).innerHTML += str1;
    }
    //默认渲染第一页
    renderPage();
 
    //点击前翻按钮
    prev.onclick = function(){
        if(page > 1){
            page--;
            renderPage();
        }
    }
    //点击后翻按钮
    next.onclick = function(){
        if(page < Math.ceil(count / 10)){
            page++;
            renderPage();
        }
    }
    //点击任意页码按钮
    pages.addEventListener('click', function (e) {
        page = e.target.getAttribute('json-page');
        renderPage();
    });
}
