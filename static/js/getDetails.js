$(document).ready(function () {
    $("#usersdetails").click(function () {
        $.ajax({
            type: "POST",
            dataType: "json",
            url: "/userLogin/capitalDetails",
            data: $("#usersDetailsOrder").serialize(),
            success: function (result) {
                if(result=="�˺���Ϣ�쳣��")
                {
                    getDetails({}, "tabDetails");
                }
                else
                {
                    getDetails(result, "tabDetails");           
                }
                alert("��ѯ�ɹ�!");
            },
            error: function () {
                alert("����ϵͳԭ���ѯʧ��!");
            }
        });
    });
});

function getDetails (json, eleId) {
    //Ĭ�ϵ�ÿҳ����¼��
    var num1 = 10;
    //ÿҳ��ʵ�ļ�¼��
    var num2;
    //Ĭ��չʾ��һҳ
    var page = 1;
 
    //�л�ǰ��ҳ���ҳ��İ�ť
    var prev = document.getElementById("prev");
    var pages = document.getElementById("pages");
    var next = document.getElementById("next");
    prev.innerHTML = "��";
    next.innerHTML = "��";
 
    //������ҳ��
    var count = Object.keys(json).length;
    //����ҳ�밴ť
    function creatPages(){
        pages.innerHTML = "";
        for(var i = 0; i < Math.ceil(count / 10); i++){
            pages.innerHTML += `<button json-page="${i+1}">\xa0${i+1}\xa0</button>`;
            //pages.innerHTML += " <button json-page='${i+1}'>"+(i+1)+" <button>";
        }
    }
    creatPages();
    
    //��Ⱦÿһҳ����������
    function renderPage(){
        //���ñ�ͷ
        var str = "<tr><th>���</th><th>����ʱ��</th><th>���׽��</th><th>���ױ���</th><th>������ϸ</th></tr>"
        document.getElementById(eleId).innerHTML = str;
 
        //�жϵ�ǰѡ���ҳ���Ӧ�ļ�¼��
        if(count - num1 * (page - 1) >= 10){
            num2 = 10;
        }
        else{
            num2 = count - num1 * (page - 1);
        }
 
        //��Ⱦ��ҳ��Ӧ������
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
    //Ĭ����Ⱦ��һҳ
    renderPage();
 
    //���ǰ����ť
    prev.onclick = function(){
        if(page > 1){
            page--;
            renderPage();
        }
    }
    //����󷭰�ť
    next.onclick = function(){
        if(page < Math.ceil(count / 10)){
            page++;
            renderPage();
        }
    }
    //�������ҳ�밴ť
    pages.addEventListener('click', function (e) {
        page = e.target.getAttribute('json-page');
        renderPage();
    });
}
