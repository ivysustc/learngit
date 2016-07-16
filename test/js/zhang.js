function fillchart(chart,valuepic){
mistakeStep = 13; //允许点击的误差范围
point = new Map();
pointValue = new Map();//值
months = new Array();//横坐标
dataset = new Array(); //全局数组
var c;
var ctx;
var part;
var pic = new Image();
pic.src = "img/qipao.png";
for(var i = 1; i < 13; i++) {
	months.push(i * 20 + 100); //横坐标元素
}

c =chart;
ctx = c.getContext("2d");
ctx.save();
ctx.beginPath();
ctx.strokeStyle = "rgb(68,67,65)";

////测试
//ctx.moveTo(0,0);
//ctx.lineTo(30,0);
//ctx.lineWidth=10;
//ctx.strokeStyle ='red';
//ctx.stroke();
//ctx.moveTo(100,200);
//ctx.lineTo(200,200);
//ctx.stroke();
////
ctx.lineWidth = 0.1;
ctx.translate(100, 200);
ctx.moveTo(0, 0);
ctx.lineTo(260, 0); //X axis
ctx.stroke();
ctx.moveTo(0, 0);
ctx.lineTo(0, -150); // Y axis
ctx.moveTo(0, 0);
ctx.fillStyle = "rgb(207,207,207)";
ctx.fillText("0", -15, 5);
ctx.fillText("20", -20, -25);
ctx.fillText("40", -20, -55);
ctx.fillText("60", -20, -85);
ctx.fillText("80", -20, -115);
ctx.fillText("100", -25, -145);

ctx.fillText("个数", -40, -175);
ctx.fillText("月份", 270, 10);
ctx.fillText("运单量", 125, -185);
ctx.strokeStyle = "rgb(207,207,207)";
for(var i = 1; i < 6; i++) {
	ctx.moveTo(0, i * (-30));
	ctx.lineTo(5, i * (-30));
	ctx.stroke();
} //Y axis
ctx.moveTo(0, 0);
ctx.lineWidth = 2;

for(var i = 1; i < 13; i++) {

	ctx.moveTo(i * 20, 0);
	ctx.lineTo(i * 20, -5);
	ctx.stroke();
} //X axis

ctx.stroke();
ctx.moveTo(0, 0);

//取得表中的数据
var tree = document.getElementsByClassName("value")[0].getElementsByTagName("td");

for(var i = 0; i < 13; i++) {
	if(i != 0) {

		dataset[i - 1] = tree[i].innerText; //获得表中的数据
		//		alert(dataset[i-1]);
		pointValue.set(months[i - 1], dataset[i - 1]);
		point.set(months[i - 1], parseInt(200 - (3 * dataset[i - 1] / 2)));

		//				alert(months[i-1]+point.get(months[i-1]));
		//					alert(tree[i].innerText);
		//					ctx.moveTo(i*20,-1*3*datavalue/2);
		//					ctx.fillRect(10,i*20,-1*3*datavalue/2);
	}
}

for(var i = 0; i < 11; i++) {
	//				alert(dataset[i]);
	ctx.lineJoin = "round";
	ctx.lineCap = "round";
	ctx.moveTo((i + 1) * 20, -1 * 3 * dataset[i] / 2);
	ctx.quadraticCurveTo((i + 1) * 20, (-1 * 1.6 * dataset[i]), (i + 2) * 20, -1 * 3 * dataset[i + 1] / 2);
	ctx.stroke();
}
ctx.restore();
//得到内部坐标
function getEventPosition(ev, x, y) {
	var x, y;
	var absolutePos = c.getBoundingClientRect();
	//	alert(absolutePos.left);
	return {
		x: x - absolutePos.left * (c.width / absolutePos.width),
		y: y - absolutePos.top * (c.height / absolutePos.height)
	};
}
//事件监听
c.addEventListener('mousemove', function(e) {
	
	p = getEventPosition(e, e.clientX, e.clientY);
	var x = parseInt(p.x);
	var y = parseInt(p.y);
	//	judgeClick(x,y);

	for(var i = 1; i < 13; i++) {
		if(parseInt(Math.abs(x - months[i - 1])) < parseInt(mistakeStep)) {
			for(var j = 1; j < 13; j++) {
				//把 map 里的 key 值转为数字
				var valueY = Math.abs(y - parseInt(point.get(months[i - 1])));
				if(parseInt(valueY) < parseInt(mistakeStep)) {
					
					loadPic1(months[i - 1]-8, point.get(months[i - 1]) - 20, pointValue.get(months[i - 1]));
					break;
				}
				break;
			}
		}
	}
});
//绘制起泡图片
function drawPic1(x, y, pic, value) {
//	var canvas2 = document.getElementById("valuePic");
//	var ctx2 = canvas2.getContext("2d");
	part = valuepic;
	y = parseInt(y)+44;	
	part.style.top=y+"px";
	part.style.left= x+"px";
	part.style.width="40px";
	part.style.height="40px";
	part.innerHTML= value;
	part.style.textAlign="center";
	part.style.lineHeight="30px";
//	par.style.backgroundImage 
//	ctx2.drawImage(pic, x, y, 25, 25);
//	ctx2.fillText(value, x + 6, y + 15);
}
//气泡图片加载
function loadPic1(x, y, value) {
	
	if(pic.complete) {
		drawPic1(x, y, pic, value);
	} else {
		pic.onload = function() {
			drawPic1(x, y, pic, value);
		}
	}
	pic.onerror = function() {
		alert("fail to load pic");
	}
}

if(document.all) {
	window.attachEvent('onload', load);
} else {
	//	window.addEventListener('load',load);
}
}
fillchart(document.getElementsByClassName("chart")[0],document.getElementsByClassName("valuePic")[0]);
fillchart(document.getElementsByClassName("chart")[1],document.getElementsByClassName("valuePic")[1]);

