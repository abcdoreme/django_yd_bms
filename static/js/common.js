$(document).ready(function(){
	//关闭低版本浏览器的屏蔽窗口
	$('#offWin').click(function(){
		$('#identify').fadeOut();
	});
	
	//禁止选中
	//document.onselectstart = function(){return false;}
	
	// 设置页面的内容区高度
	var windowH = $(window).height();
	$('#main').css('height',windowH - 64);



	//设置导航部分
	$('.nav-left a.nav-list').hover(function(){
		var i = $(this).index();
		navStyle(i);
		$(this).css({'color':'#4367bd','background':'#f3f3f3'});
	},function(){
		var i = $('.nav-left a.active').index();
		if(!$(this).is('.active')){
			$(this).css({'color':'#4f5976','background':'#c0c8db'});
		}
		navStyle(i);
	})
	function navStyle(t){
		var line = $('.nav-left .line');
		line.css({'top':t * 60,'transition':'cubic-bezier(0.015, 0.695, 0.34, 1.365) 0.2s'});
	}
	function listMouseout(){
		var i = $('.nav-left a.active').index();
		navStyle(i);
	}
	listMouseout();

	//提交按钮
	$('.inbox .sub').hover(function(){
		var i = $(this).index();
		$(this).css({'background':'#c0c8db', 'cursor':'pointer'});
	},function(){
		$(this).css({'background':'#cfcfcf'});
	})
	
//	退出登录
	$("#user_name").click(function(){
		$("#win,#win .logout").fadeIn();
	})
//确定退出
	$("#win .logout .okbtn").click(function(){
		//注销
		window.location="${pageContext.request.contextPath}/logout.action";
	})
//取消退出登录	
	$("#win .logout .cancelbtn").click(function(){
		$(this).parent().fadeOut().end().parent().parent().fadeOut();
	})

	    //关闭弹窗
    $(".winbox .tit a").click(function(){
        $('#wenben').show();
        $('#json-renderer').hide();
        $(this).parents('.masks').fadeOut();
        if($(this).attr("type-i") == "2"){
            $("#autotc").children(".winbox").children(".configuration_nav").children('li').eq(0).addClass("active").siblings().removeClass('active');
            $("#autotc").children(".winbox").children(".tc-tab-box").children().eq(0).show().siblings().hide();
            $("#test_input1,#test_input2,#test_input3,#test_input4").val("");
            $("#autotesting tbody").html("");
            $("#paging2 .pages em").text('5');
            $("#paging2 .pages li").eq(0).addClass('on').siblings().removeClass('on');
        }
        // window.location.realod();
    });

	 //开机任务配置点击
    $(".tables-box table").on('click','.setbtnB',function(){
        $('.listConfig').hide();
        a(this,"prel","1");
        
    })
    
    //周期任务配置点击
    $(".tables-box table").on('click','.setbtnP',function(){
        $('.listConfig').show();
        a(this,"prel","2");
        
    })

    //查看数据点击
    $(".tables-box table").on('click','.setbtnK',function(){
        //window.location.reload();
        b(this,"prel","3");
       // console.log(this)
        
    })


    //回显任务配置信息
    function a(btn,tag,tagStr){
        $('#wenben').show();
        $('#json-renderer').hide();
        $('.sub').show();
        // $('.sub2').hide();
        $("#wenben").html("");
        $('.masks').fadeIn();
        var sn = $(btn).parent().parent().find("td:eq(1)").html();
        $(".testCount").val("");
        document.getElementById("isOpen").checked=false;
        $("#fitSn").val(sn);
        $("#snName").html(sn);
        if(tagStr == "1"){
            $("#tagStr").html("开机");
            $("#tagStrs").val("1");

        }else{
            $("#tagStr").html("周期");
            $("#tagStrs").val("2");
        }   

        $.get("/searchBootConfig",{"bootSn":sn, "tagStr":tagStr},function(data,status){

            var configInfo = eval("("+data+")");
            informationmessage = configInfo.configInfo;
            $("#wenben").html(informationmessage);
            var isOpen = configInfo.isOpen;
            if(isOpen == 'true'){
                document.getElementById("isOpen").checked=true;
                $(".testCount").val(configInfo.testCount);
            }
        }); 
    }

    var informationmessage = "";
    //查看上报数据
    function b(btn,tag,tagStr){

        $("#wenben").html("");
        $('.masks').fadeIn();

        $('.sub').hide();
        $('.sub2').show();
        var sn = $(btn).parent().parent().find("td:eq(1)").html();
        var information = $(btn).parent().parent().find("td:eq(6)").html();
        informationmessage = information;
        $("#fitSn").val(sn);
        $("#snName").html(sn);
        $("#tagStr").html(name);

        $("#wenben").html(information);
        console.log(sn);
    }

    //点击数据
    $(".changeMessage1").click(function(){
        $('#wenben').show();
        $('#json-renderer').hide();
        // $('.listConfig').hide();
        
        $("#wenben").html(informationmessage);
    })

    //点击格式化json
    $(".changeMessage2").click(function(){
        $('#wenben').hide();
        $('#json-renderer').show();
        // $('.listConfig').hide();
        var information = $("#wenben").html();
        formatJson(informationmessage);
    })

    $(".aTl").click(function(){//上一页	aTl
        var prevNum = (pageNum-1)<=0?1:(pageNum-1);
        window.location.href="/"+tag+"?bootSn="+sn+"&bootTimeStart="+bootTimeStart+"&bootTimeEnd="+bootTimeEnd+"&pageNum="+prevNum+"&pageSize="+pageSize;
    })

    $(".aTr").click(function(){//下一页	aTr
        var nextNum = (pageNum+1)>countPage?countPage:(pageNum+1);
        window.location.href="/"+tag+"?bootSn="+sn+"&bootTimeStart="+bootTimeStart+"&bootTimeEnd="+bootTimeEnd+"&pageNum="+nextNum+"&pageSize="+pageSize;
    })
    $(".aTg").click(function(){//跳转到第n页	aTg
        var num = $('.pagePage').val();
        if(Number(num) <=0){
            num = 1
        }else if(Number(num) > countPage){
            num = countPage;
        }

        window.location.href="/"+tag+"?bootSn="+sn+"&bootTimeStart="+bootTimeStart+"&bootTimeEnd="+bootTimeEnd+"&pageNum="+num+"&pageSize="+pageSize;
    })

      //厂商点击
    $(".manufacturer dd:nth-child(2) span").click(function(){
        pageNum = 1;
        $(this).addClass("active").siblings().removeClass("active");
        var stbCode = $(this).attr("stbcode");
        var listLeng = $("#paging1 .pages li.on").text();
        window.location.href="/"+tag+"?bootSn="+stbCode+"&bootTimeStart="+bootTimeStart+"&bootTimeEnd="+bootTimeEnd+"&pageNum="+pageNum+"&pageSize="+pageSize;
    })

        //地图厂商点击
      $(".manufacturer2 dd:nth-child(2) span").click(function(){
        $(this).addClass("active").siblings().removeClass("active");
        var stbCode = $(this).attr("stbcode");
        var listLeng = $("#paging1 .pages li.on").text();
        window.location.href="/"+tag+"?manu="+stbCode+"&bras="+bras+"&olt="+olt+"&addr="+addr+"&street="+street+"&bootSn="+map;
    })

        //SN搜索
    $(".search").click(function(){	
        pageNum = 1;
        var bootSn = document.getElementById('bootSn').value;
        var bootTimeStart = document.getElementById('bootTimeStart').value;
        var bootTimeEnd = document.getElementById('bootTimeEnd').value;
        var sel = document.getElementById('sel').value;
        window.location.href="/"+tag+"?bootSn="+bootSn+"&sel="+sel+"&bootTimeStart="+bootTimeStart+"&bootTimeEnd="+bootTimeEnd+"&pageNum="+pageNum+"&pageSize="+pageSize;
    })
	
	//设置点击左侧导航
    $(".nav-left a").on('click',function(){
        window.location.href='/'+$(this).attr('stbcode');
    })

    //左侧导航栏设置
    function navscrollTop() {
        // let navH=$(".nav-left").height();
        // //let navHlength=$(".nav-left a").length;
        // let index=$('.'+tag).index();
        // let itemTop=(index+1)*60;
        // let diffvalue=itemTop-navH+20;
        // //let scrollHeight=$('.nav-left').prop("scrollHeight");
        // //alert('itemTop:'+itemTop+'navH:'+navH+'diffvalue:'+diffvalue)
        // $(".nav-left").scrollTop(diffvalue)
    }
    navscrollTop();
    
    //日期格式转换
    function dateFormat(datetime){
        var dateStr=datetime.toString();
        var year=dateStr.slice(0,4);
        var month=dateStr.slice(4,6);
        var day=dateStr.slice(6,8);
        var newdate=year+"-"+month+"-"+day;
        return newdate;
    };

    // MAC地址校验
    function isValidMacAddress(mac) {
        // 正则表达式解释：
        // ^ 表示字符串开始
        // [0-9A-Fa-f]{2} 表示2个十六进制数字（0-9或A-F或a-f）
        // (:[0-9A-Fa-f]{2}){5} 表示有5个组，每组由冒号和2个十六进制数字组成
        // | 表示或
        // - 表示短横线（-）
        // $ 表示字符串结束
        // const macRegex = /^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$/;
        // 先判断是不是单播MAC
        var h = parseInt(mac.slice(0, 2), 16);
        if(h % 2){
            return false;
        }
        // MAC地址不带冒号或短横线
        const macRegex = /^[0-9A-Fa-f]{12}$/;;
        return macRegex.test(mac);
    }
    
    // GPON SN校验
    function isValidGponSn(sn) {
        // 4个可读字符+4个十六进制数字
        const snRegex = /^([0-9A-Za-z]{4})([0-9A-Fa-f]{8})$/;
        return snRegex.test(sn);
    }

})