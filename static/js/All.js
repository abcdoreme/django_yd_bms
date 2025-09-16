/**
 * 
 * @authors Your Name (you@example.org)
 * @date    2015-12-16 14:44:03
 * @version $Id$
 */
;(function($){
	//调用方法如下：
	//jQuery.getMonth(data)ele,xData,n,data
    
    //饼图3.0
    $.extend({
    	cpuLine: function(ele,xData,n,data){//ele:父元素   rad：饼图半径   data：数据
    		// 基于准备好的dom，初始化echarts实例
            var myChart = echarts.init(document.getElementById(ele));

            // 指定图表的配置项和数据
            var option = {
            	tooltip: {
    		        trigger: 'axis',
    		        axisPointer : {            // 坐标轴指示器，坐标轴触发有效
    		            type : 'line',         // 默认为直线，可选为：'line' | 'shadow'
    		            lineStyle : {          // 直线指示器样式设置
    		                color: '#cad2e7',
    		                width: 1,
    		                type: 'solid'
    		            }
    		        },
    		    },
    		    color:['#4e6fc0'],
    		    grid: {
    		    	top: '15',
    		    	left: '3%',
    		        right: '4%',
    		        bottom: '2%',
    		        containLabel: true
    		    },
                xAxis: {
                	type: 'category',
                	//name: 'aaa',
            		//boundaryGap: false,
                	boundaryGap: ['2%', '3%'],
            		axisLabel:{  //x轴的值挺斜设置
    	            	//rotate:45,//x轴数值旋转角度
    	            	textStyle:{
    	            		color:'#535353'
    	            	}
    	            },
            		axisLine: {
    	                lineStyle: {
    	                	color: '#cad2e7',
    	                    type: 'solid',
    	                    width: 2
    	                }
    	            },
    	            splitLine : {    //设置X轴网格颜色
    	                show:false
    	            },
                    data: xData
                },
                yAxis: {
                	type: 'value',
                	axisLine: {
                		show:false
    	            },
    	            axisTick: {
    	            	show: false
    	            },
    	            splitLine : {    //设置X轴网格颜色
    	            	lineStyle: {
    	                	color: '#cad2e7',
    	                    type: 'solid',
    	                    width: 1
    	                }
    	            },
                },
                series: [{
                    name: n,
                    type: 'line',
                    data: data
                }]
            };

            // 使用刚指定的配置项和数据显示图表。
            myChart.setOption(option);
    	}
    });

    
    
})(jQuery);