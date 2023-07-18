<?php

// 发送短信报警
$url = 'http://web.wasun.cn/asmx/smsservice.aspx';

// 短信数组
$data = array(
	'name' => 'xxxxxxxxxxxx', //用户名
	'pwd' => 'xxxxxxxxxxxxxxxxx', //密码
	'content' => '', //运维短信通过的审核模板为【医教园运维】IP：@，监控项目：@， 级别：@
	'mobile' => '', //发送的手机号码,多个号码用逗号隔开
	'sign' => '【xxxxxxxxxxx】', //必填参数.用户签名
	'type' => 'xxxxxxxx' //必填选项 固定值pt
);

// 接收命令行参数
//var_dump($argv[2]);
$data['mobile'] = $argv[1];
//$data['content'] = $argv[2];
$data['content'] = 'IP：192.168.0.1，监控项目：nginx 级别：宕机';

$o = '';
foreach ($data as $k => $v){
	if ($k == 'content')
		$o .= $k .= '=' . urlencode($v) . '&';
	else
		$o .= $k .= '=' . ($v) . '&';
}
$post_data = substr($o,0,-1);
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 5);
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_POSTFIELDS, $post_data);
$result = curl_exec($ch);
echo $result
?>
