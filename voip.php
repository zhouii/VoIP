<!--
Code by Bluecat
https://github.com/zhouii/VoIP
-->
<?php
if (in_array($_POST['action'], ['query','enable','disable','switch'])) {
	echo exec('python3 voip.py '.$_POST['action']);
	exit;
}
?>
<!DOCTYPE html>
<html>
<head>
	<meta charset="UTF-8">
	<title>VoIP</title>
	<meta name="viewport" content="width=device-width, user-scalable=no" />
	<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />
	<link rel="stylesheet" href="https://cdn.staticfile.org/twitter-bootstrap/3.4.1/css/bootstrap.min.css">
	<!--[if IE]><script type="text/javascript" src="https://cdn.staticfile.org/jquery/1.12.4/jquery.min.js"></script><![endif]-->
	<!--[if !IE]>--><script type="text/javascript" src="https://cdn.staticfile.org/jquery/3.4.1/jquery.min.js"></script><!--<![endif]-->
	<script src="https://cdn.staticfile.org/twitter-bootstrap/3.4.1/js/bootstrap.min.js"></script>
	<style>
		.spinner {
			margin: 50px auto;
			width: 60px;
			height: 100px;
			text-align: center;
			font-size: 10px;
		}

		.spinner > div {
			background-color: #939f9e;
			height: 100%;
			width: 8px;
			display: inline-block;
			-webkit-animation: stretchdelay 1.2s infinite ease-in-out;
			animation: stretchdelay 1.2s infinite ease-in-out;
		}

		.spinner .rect2 {
			-webkit-animation-delay: -1.1s;
			animation-delay: -1.1s;
		}

		.spinner .rect3 {
			-webkit-animation-delay: -1.0s;
			animation-delay: -1.0s;
		}

		.spinner .rect4 {
			-webkit-animation-delay: -0.9s;
			animation-delay: -0.9s;
		}

		.spinner .rect5 {
			-webkit-animation-delay: -0.8s;
			animation-delay: -0.8s;
		}

		@-webkit-keyframes stretchdelay {
			0%, 80%, 100% { -webkit-transform: scaleY(0.6) } 
			40% { -webkit-transform: scaleY(1.0) }
		}

		@keyframes stretchdelay {
			0%, 80%, 100% {
				transform: scaleY(0.6);
				-webkit-transform: scaleY(0.6);
			}  40% {
				transform: scaleY(1.0);
				-webkit-transform: scaleY(1.0);
			}
		}
		#waiting{
			position: fixed;
			text-align: center;
			display: none;
			margin: auto;
			height: 100%;
			width: 100%;
			background: rgba(255, 255, 255, 0.7);
			z-index:2000;  
		}
	</style>
</head>
<body style="background-color: #f2f2f2; text-align: center; ">
	<div id="waiting">
		<h1>请稍候</h1>
		<div class="spinner">
			<div class="rect1"></div>
			<div class="rect2"></div>
			<div class="rect3"></div>
			<div class="rect4"></div>
			<div class="rect5"></div>
		</div>
	</div>
	<div style="margin: auto; max-width: 600px; padding: 20px; ">
		<h3>VoIP开关</h3>
		<div class="row" style="margin: auto; line-height: 60px;">
			<div class="col-xs-6"><button type="button" class="btn btn-default" data-action="query">查询状态</button></div>
			<div class="col-xs-6"><button type="button" class="btn btn-warning" data-action="switch">切换状态</button></div>
			<div class="col-xs-6"><button type="button" class="btn btn-success" data-action="enable">打开VoIP</button></div>
			<div class="col-xs-6"><button type="button" class="btn btn-danger" data-action="disable">关闭VoIP</button></div>
		</div>
		<div class="modal fade" id="myAlert" tabindex="-1" role="dialog">
			<div class="modal-dialog" role="document">
				<div class="modal-content">
					<div class="modal-body">
					</div>
					<div class="modal-footer">
						<button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>
					</div>
				</div>
			</div>
		</div>
	</div>
	<script>
		function myAlert(txt){
			$('.modal-body').html(txt);
			$('#myAlert').modal('show');
		}
		function lock() {
			$('#waiting>h1').css('margin-top',$(window).height()/2-100);
			$('#waiting').show();
		}
		function unlock() {
			$('#waiting').hide();
		}
		$('[data-action]').click(function(){
			lock();
			$.ajax({
				type:'post',
				data:{
					action:$(this).data('action')
				},
				success:function(res){
					unlock();
					if (res!='1' && res!='2') myAlert('操作失败！');
					else myAlert('操作成功！操作后VoIP处于'+(res=='1'?'关闭':'开启')+'状态');
				},
				error:function(){
					unlock();
					myAlert('操作失败！');
				}
			});
		});
	</script>
</body>
</html>
