<?php
	$base_url="http://www.widuu.com/archives/";
	$urls=array();
	$db_name='climb_data';
	$table_name=str_replace('.', '_', split("/", $base_url)[2]);
	try {
		$pdo = new PDO('mysql:host=localhost;dbname='.$db_name,'root','123456');
		$sql = "insert into ".$table_name."(video_url)"."values(?)";
		$stmt=$pdo->prepare($sql);
		//$stmt->bindParam(1,$v_u);
		for($i=1;$i<100;$i++){
			for($j=1;$j<1000;$j++){
				$url=$base_url.$i."/".$j;
				$content = file_get_contents($url);
				echo $url."\n\r";
				if(strstr($content, "flashvars") ){//防止404
					//array_push($urls, $content);
					echo $url;exit;
					$stmt->bindParam(1,$v_u);
					$v_u=$url;
					$stmt->execute();
				}
			}
		}
		$pdo = null;exit; 
	}   
    catch (Exception $e) {
		echo "Error:".$e->getMessage()."\n\r";
		die();
	}
	
?>