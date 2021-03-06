# coding:utf-8
import time
import re

migu_html = '''<!DOCTYPE html>
<html>
<head>
<meta name="viewport"
	content="width=device-width,initial-scale=1,minimum-scale=1,maximum-scale=1,user-scalable=no" />
<title></title>
<link rel="stylesheet" type="text/css" href="css/media720.css" />
<link rel="stylesheet" type="text/css" href="css/layout.css" />
<!-- <script type="text/javascript" src='http://wap.dm.10086.cn/apay/migu.js'></script> -->
<script type="text/javascript" src='http://wap.dm.10086.cn/apay/migu.js'></script>

</head>
<script type="text/javascript">
	var http_request = false;
	var i = 120;
	var webOrderId = '';
	var webNoticleUrl = '';
	var prodcutId = '';
	migusdk.init('b35c935ea09b4f5e9a75ebad0502e46b', function(resultCode, msg, authSessionId){
//         alert("init resultCode = " + resultCode);
		if (resultCode === '0000'){
//         	alert("发送session:"+authSessionId+" 到服务器223.111.8.142 8080");
        	url = 'http://wap.dm.10086.cn/apay/session.jsp?netId=b35c935ea09b4f5e9a75ebad0502e46b&authId=8f6c153968e942f0b33c29b5d7c1934a&authSessionId='+authSessionId;
        	httpGet(url, callbackSessionId);
       }else{
    	    alert("初始化sdk 失败");
       }
    },'Common');

	function webGetOrderId(){
		var msisdn = document.getElementById("msisdn").value;
		if (msisdn == "") {
			alert("手机号码为空！");
			return;
		} else {
			var type = 2;
			var PayType = '';
			if(type == "2"){
				PayType = '1031';
			}else{
				PayType = '1021';
			}
			var url = "handle.jsp?t=webGetOrderId&paycode="+300008025001+"&sss="+1811091187+"&channelId="+700000924+"&msisdn="+msisdn+"&PayType="+PayType;
			httpGet(url, callbackWebGetOrderId);
		}
	}

	function changeImg(){
		var Num="";
		for(var i=0;i<6;i++)
		{
			Num+=Math.floor(Math.random()*10);
		}
		var path = "http://wap.dm.10086.cn/capability/capacc/imgCode"+'?session='+1811091187+'&randnum='+Num;
		var img = document.getElementById("authCodeImg");
		img.src = path;
	}

	function checkSmsCode(){
		var CheckSmsCode = document.getElementById("CheckCode").value;
		if (CheckSmsCode == "") {
			alert("请输入短信验证码！");
			return;
		} else {
			var url = "handle.jsp?t=checkSmsCode&paycode="+300008025001+"&sss="+1811091187+"&smsCode="+CheckSmsCode;
			httpGet(url, callbackCheckSmsCode);
		}
	}

	function checkImgCode(){
		var CheckImgCode = document.getElementById("authCodeInput").value;
		if (CheckImgCode == "") {
			alert("请输入图形验证！");
			return;
		} else {
			var url = "handle.jsp?t=checkImgCode&paycode="+300008025001+"&sss="+1811091187+"&answer="+CheckImgCode;
			httpGet(url, callbackCheckImgCode);
		}
	}

	function getCheckCode() { //短信验证码发送接口访问
		var msisdn = document.getElementById("msisdn").value;
 		var paycode = '300008025001';
 		var sessionid = '1811091187';
 		var orderId = '1479977252400';
//         var regx = /^(((13[0-9]{1})|(15[0-9]{1})|(18[0-9]{1}))+\d{8})$/;
        var regx = /^(((13[0-9]{1})|(14[0-9]{1})|(15[0-9]{1})|(18[0-9]{1}))+\d{8})$/;
        if (!regx.test(msisdn)) {//判断手机号码是否合法
			alert("请输入正确的手机号码！");
			return false;
		} else {
			i = 120; // reset i here
			countDown();
			var url = "handle.jsp?t=checkcode&paycode="+paycode+"&sss="+sessionid+"&order="+orderId+"&msisdn="+msisdn;
			httpGet(url, callbackgetSmsCode);
		}
    }

	function countDown() {//倒计时功能实现
		if (i == 0) {
			document.getElementById("sendSMS").setAttribute("value", "发送验证码 ");
			document.getElementById("sendSMS").disabled = false;
			return;
		}
		document.getElementById("sendSMS").disabled = true;
		document.getElementById("sendSMS").setAttribute("value", i + "秒后重发");
		i--;
		setTimeout("countDown();", 1000);
	}

	function callbackWebGetOrderId(){
		if (http_request.readyState == 4) {
			if (http_request.status == 200) {
				var json_txt = http_request.responseText;
				var json_data = eval("(" + json_txt + ")");
				var returnCode = json_data.ReturnCode;
				if(returnCode == 0){
// 					alert('订购ID获取成功');
					webOrderId = json_data.webGetOrderId;
					webNoticleUrl = json_data.noticeUrl;
					prodcutId = json_data.BossId;
					var type = 2;
					if(type == "2"){
// 						alert('包月订购');
// 						alert('prodcutId=[' + prodcutId +']');
						payMonthly();
					}else{
// 						alert('点播订购');
	 					pay();
					}
				}else if(returnCode == 1){
					returnCode = '0005';
					window.location.href = "errorPage.jsp?returnCode="
						+ returnCode;//根据返回码返回到错误页面
				}else if(returnCode == 2){
					returnCode = '0006';
					window.location.href = "errorPage.jsp?returnCode="
						+ returnCode;//根据返回码返回到错误页面
				}else{
					window.location.href = "errorPage.jsp?returnCode="
							+ returnCode;//根据返回码返回到错误页面
				}
			} else {
				alert('There was a problem with the getWebOrderid request.[' + http_request.status +']');//接口访问失败返回警告
			}
		}
	}

	function callbackCheckSmsCode(){
		if (http_request.readyState == 4) {
			if (http_request.status == 200) {
				var json_txt = http_request.responseText;
				var json_data = eval("(" + json_txt + ")");
				var returnCode = json_data.ReturnCode;
				if(returnCode == 0){
// 					alert('短信验证成功');
					webGetOrderId();
// 					payMonthly();
				}else if(returnCode == 1){
					alert('短信验证失败');
				}else{
					window.location.href = "errorPage.jsp?returnCode="
							+ returnCode;//根据返回码返回到错误页面
				}
			} else {
				alert('There was a problem with the checkSmsCode request.[' + http_request.status +']');//接口访问失败返回警告
			}
		}
	}

	function callbackgetSmsCode(){
		if (http_request.readyState == 4) {
			if (http_request.status == 200) {
				var json_txt = http_request.responseText;
				var json_data = eval("(" + json_txt + ")");
				var returnCode = json_data.ReturnCode;
				if(returnCode == 0){
// 					alert('短信获取成功');
				}else if(returnCode == 1){
					alert('短信验证码输入错误');
				}else{
					window.location.href = "errorPage.jsp?returnCode="
							+ returnCode;//根据返回码返回到错误页面
				}
			} else {
				alert('There was a problem with the checkImgCode request.[' + http_request.status +']');//接口访问失败返回警告
			}
		}
	}

	function callbackCheckImgCode(){
		if (http_request.readyState == 4) {
			if (http_request.status == 200) {
				var json_txt = http_request.responseText;
				var json_data = eval("(" + json_txt + ")");
				var returnCode = json_data.ReturnCode;
				if(returnCode == 0){
// 					alert('图形验证码输入正确');
 					var v1 =  document.getElementById("sendSMS");
 					var v2 = document.getElementById("authCodeSwitch");
 					v1.disabled="";
 					v1.style.color="black";
 					v2.disabled="disabled";
				}else if(returnCode == 1){
					alert('图形验证码输入错误');
				}else{
					window.location.href = "errorPage.jsp?returnCode="
							+ returnCode;//根据返回码返回到错误页面
				}
			} else {
				alert('There was a problem with the checkImgCode request.[' + http_request.status +']');//接口访问失败返回警告
			}
		}
	}

	function pay() {//支付接口访问
		var channelId = '700000924';
		var cpId = 'CP1253';
		var payCode = '300008025001';
// 		var contentId = "WY" + payCode;
		var contentId = payCode;

		var requestIdTmp = '47196787937544';
		var pay = {};
		pay.payType = 1;
		pay.payMethod = "";
		pay.fee = 10;
		pay.orderId = webOrderId;
		pay.description = "";
		pay.channelID = channelId;
		pay.productID = "";
		pay.cpID = cpId;
		pay.contentID = contentId;
		pay.Cpparam = requestIdTmp;
// 		pay.vasType = "4";
// 		pay.servType = '200';
// 		pay.channelClass = "";
// 		pay.spCode = "";
// 		pay.memberType = "1";
// 		pay.ctype ="4";
		pay.saleType = '401';
		pay.settleDate = "";
		pay.netId = 'b35c935ea09b4f5e9a75ebad0502e46b';
		var str = JSON.stringify(pay);
		migusdk.pay(str, function(resultCode, msg, paydata){
// 		    alert(resultCode);
// 		    alert(msg);
			if (resultCode === '0000'){
// 				var url = "handle.jsp?t=GetWebCallbackAddrReq&paycode="+paycode+"&sss="+sessionid+"&order="+orderId+"&msisdn="+msisdn;
// 				httpGet(url, callbackAddrReq);

				var noticeurl = webNoticleUrl;
				window.location.href = "orderSuccess.jsp?totalprice="
						+ 0.10  + "&telephone=" + 4006738638 + "&orderId=" + 1479977252400 + "&noticeUrl=" + noticeurl + "&orderType=" + 2;
			}else{
				window.location.href = "errorPage.jsp?returnCode="
					+ resultCode;
			}
		});
	}

	function payMonthly() {//支付接口访问
		var channelId = '700000924';
		var cpId = 'CP1253';
		var payCode = '300008025001';
		var requestIdTmp = '47196787937544';
		var pay = {};
		pay.payType = 7;
		pay.operCode = "01";
		pay.spCode = "698025";
		pay.fee = 10;
		pay.orderId = webOrderId;
		pay.vasType = "4";
		pay.description = "";
		pay.channelID = channelId;
		pay.productID = prodcutId;
		pay.cpID = cpId;
		pay.Cpparam = requestIdTmp;
		pay.netId = 'b35c935ea09b4f5e9a75ebad0502e46b';
		var str = JSON.stringify(pay);
		migusdk.pay(str, function(resultCode, msg, paydata){
// 		    alert(resultCode);
// 		    alert(msg);
			if (resultCode === '0000'){
// 				var url = "handle.jsp?t=GetWebCallbackAddrReq&paycode="+paycode+"&sss="+sessionid+"&order="+orderId+"&msisdn="+msisdn;
// 				httpGet(url, callbackAddrReq);

				var noticeurl = webNoticleUrl;
				window.location.href = "orderSuccess.jsp?totalprice="
						+ 0.10  + "&telephone=" + 4006738638 + "&orderId=" + 1479977252400 + "&noticeUrl=" + noticeurl + "&orderType=" + 2;
			}else{
				window.location.href = "errorPage.jsp?returnCode="
					+ resultCode;
			}
		});
	}

	function httpGet(url, callback) {
		//接口调用函数
		http_request = false;
		if (window.XMLHttpRequest) {// code for IE7+, Firefox, Chrome, Opera, Safari
			http_request = new XMLHttpRequest();
		} else if (window.ActiveXObject) {// code for IE6, IE5
			try {
				http_request = new window.ActiveXObject("Msxml2.XMLHTTP");
			} catch (e) {
				try {
					http_request = new window.ActiveXObject("Microsoft.XMLHTTP");
				} catch (e) {
					alert('Giving up :( Cannot create an XMLHTTP instance');
					return false;
				}
			}
		}
		http_request.onreadystatechange = callback;
		http_request.open('GET', url, true);
		http_request.send();
	}

	function callbackAddrReq() {
		if (http_request.readyState == 4) {
			if (http_request.status == 200) {
// 				alert("http_request.status == 200");
				var json_txt = http_request.responseText;
				var json_data = eval("(" + json_txt + ")");
				var returnCode = json_data.ReturnCode;
				var address = json_data.Address;
				if (returnCode == 0) {
					address += "&status=0";
					var totalprice = '0.10 ';
					var telephone = '4006738638';
					var orderId = '1479977252400';
					var orderType = '1';

					window.location.href = "orderSuccess.jsp?totalprice="
							+ totalprice + "&telephone=" + telephone + "&orderId=" +orderId + "&noticeUrl=" + address + "&orderType=" + orderType;
				} else {
// 					alert('There was a problem with the orderConfirm request.[' + returnCode +']');
					window.location.href = "errorPage.jsp?returnCode="
							+ returnCode;
				}
			} else {
				alert('There was a problem with the orderConfirm request.[' + http_request.status +']');
			}
		}
	}

	function callbackSessionId() {
		if (http_request.readyState == 4) {
			if (http_request.status == 200) {
// 				alert("http_request.status == 200");
				var json_txt = http_request.responseText;
				var json_data = eval("(" + json_txt + ")");
				var msg = json_data.msg;
				var returnCode = json_data.resultCode;
				if (returnCode == '0000') {
					alert("sessionId send success!");
				} else {
// 					alert('There was a problem with the orderConfirm request.[' + returnCode +']');
					window.location.href = "errorPage.jsp?returnCode="
							+ returnCode;
				}
			} else {
// 				alert('There was a problem with the orderConfirm request.[' + http_request.status +']');
			}
		}
	}

	function callbackPay() {//支付确认回调函数
		if (http_request.readyState == 4) {
			if (http_request.status == 200) {
// 				alert("http_request.status == 200");
				var json_txt = http_request.responseText;
				var json_data = eval("(" + json_txt + ")");
				var returnCode = json_data.ReturnCode;
				var noticeUrl = json_data.NoticeUrl;
				if (returnCode == 0) {
					noticeUrl += "&status=0";
					var totalprice = '0.10 ';
					var telephone = '4006738638';
					var orderId = '1479977252400';
					var orderType = '1';

					window.location.href = "orderSuccess.jsp?totalprice="
							+ totalprice + "&telephone=" + telephone + "&orderId=" +orderId + "&noticeUrl=" + noticeUrl + "&orderType=" + orderType;
				} else {
// 					alert('There was a problem with the orderConfirm request.[' + returnCode +']');
					window.location.href = "errorPage.jsp?returnCode="
							+ returnCode;
				}
			} else {
				alert('There was a problem with the orderConfirm request.[' + http_request.status +']');
			}
		}
	}
</script>
<body>
	<div class="txt">
		<table>
			<tr>
				<td class="td1">应用名称:</td>
				<td class="td2">学习资源网会员包</td>
			</tr>
			<tr>
				<td class="td1">提供商:</td>
				<td class="td2">北京疯狂青蛙科技有限公司</td>
			</tr>
			<tr>
				<td class="td1">资费:</td>
				<td class="td2">0.10 元/月</td>
			</tr>
			<tr>
				<td class="td1">客户电话:</td>
				<td class="td2">4006738638</td>
			</tr>
			<tr id="tr3">
				<td class="td1">图形验证:</td>
				<td class="td3">
					<div>
							<input type="text" class="_text" placeholder="点击图片换一张"
								id="authCodeInput" />
							<input type="button" id="authCodeSwitch" value="确认"
								class="_button" onclick="checkImgCode();">
					</div>
				</td>
			</tr>
			<tr id="tr4" >
				<td class="td1"></td>
				<td class="td1">
					<div >
						<img src="http://wap.dm.10086.cn/capability/capacc/imgCode?session=1811091187&randnum=917389" alt="验证码" id="authCodeImg" onclick="changeImg()" style="vertical-align:right;" width="200" height="60"/>
					</div>
				</td>
			</tr>
			<tr id="tr1" >
				<td class="td1">手&nbsp;机&nbsp;号:</td>
				<td class="td3"><div>
						<input type="text" class="_text" id="msisdn" placeholder="请输入手机号码" />
				</div></td>
			</tr>
			<tr id="tr2">
				<td class="td1">验&nbsp;证&nbsp;码 :</td>
				<td class="td3">
				<div>
					<input type="text" class="_text" placeholder="请输入验证码"
						id="CheckCode" />
					<input type="button" disabled="disabled" id="sendSMS" value="获取验证码"
						class="_button" onclick="getCheckCode();">
				</div>
				</td>
			</tr>
		</table>
	</div>
	<div class="btn">
		<a class="c" href="javascript:void(0);" onclick="checkSmsCode();">提交</a>
	</div>
	<div class="tip">
		<div class="tip_title">温馨提示</div>
		<div class="tip_con">
			本次支付<span>0.10 元/月</span>，点击确认提交即可同意发送短信以确认付费，本次支付由“咪咕动漫有限公司”提供，信息费<span>0.10 元/月</span>（不含通信费），由中国移动代收，短信提醒“<strong>手机动漫信息费</strong>”，返回或者取消本次充值不扣费。客服电话：4006738638
		</div>
	</div>
	<div class="bottom_txt">扫黄打非·净网2015，举报邮箱dm10086@139.com</div>
</body>
</html>'''

BLOCK_START = ['{']
BLOCK_END = ['}']


def parse():
    index = migu_html.find('function callbackWebGetOrderId(){')
    str1 = migu_html[index]

    print(str1)
    find_code_block(index)

"""migu init"""
def parse_migu_init():
    code = find_code_block(migu_html,'migusdk.init(')
    # print(code)


    # 将正则表达式编译成Pattern对象
    pattern = re.compile(r"http.*?\;")
    # 使用Pattern匹配文本，获得匹配结果，无法匹配时将返回None
    match = pattern.search(code)
    if match:
        print(match.group())

"""migu change img"""
def parse_change_img():
    code = find_code_block(migu_html, 'function changeImg(){')
    # print(code)
    # 将正则表达式编译成Pattern对象
    pattern = re.compile(r"http.*?\;")
    # 使用Pattern匹配文本，获得匹配结果，无法匹配时将返回None
    match = pattern.search(code)
    if match:
        result = match.group()
        result = result.replace('"', '').replace('+','').replace('\'','').replace(';','')
        print(result)


"""找到代码块 todo暂时没考虑注释情况"""
def find_code_block(html_str, code_str):
    index = html_str.find(code_str)
    html_len = len(html_str)
    block_count = 0
    is_begin = False
    end_index = index

    while True:
        if end_index >= html_len-1:
            break
        end_index += 1
        temp = html_str[end_index]
        if temp in BLOCK_START:
            block_count += 1
            is_begin = True
        if temp in BLOCK_END:
            block_count -= 1
        if is_begin and block_count == 0:
            break

    return html_str[index:end_index+1]



if __name__ == '__main__':
    parse_migu_init()
    parse_change_img()
    # s = 'abc'
    # print(s[0:2])
