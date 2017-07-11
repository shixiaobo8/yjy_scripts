<?php
   class file{
	/** php 获取文件扩展名的5中方式 */
	private $files = array();
	private $dirs = array();
	private $file_extensions = array();

	public function getFiles(){
		return $this->files;
	}

	public function getDirs(){
		return $this->dirs;
	}

	//获取当前的文件或者目录的绝对路径
	public function getrealpath($dir,$type=""){
		chdir(dirname($dir));
		$this->dirs[$dir]=array();
		// in_array()判断数组中是否存在元素,存在返回true,不存在返回false
		$v_exist = in_array($dir,$this->dirs);
		if(!$v_exist){
			$this->dirs[$dir]['基本根目录']=$dir;
			$this->dirs[$dir]['子目录有']=array();
			$this->dirs[$dir]['子文件有']=array();
		}
		if($type == "dir"){
			$dir_arrs = $this->dirs[$dir]['子目录有'];
			if(count($dir_arrs) == 0){
				array_push($dir_arrs,$dir);
			}else{
				$dir_values = array_count_values($dir_arrs);
				if($dir_values[$dir] < 1 ){
					array_push($dir_arrs,$dir);
				}
				$this->ByStrChr($dir);
			}
		}
		if($type == "file"){
			$file_arrs = $this->dirs[dirname($dir)]['子文件有'];
			$file_values = array_count_values($dir_arrs);
			if($dir_values[$dir] < 1 ){
				array_push($dir_arrs,$dir);
			}
		}
			// 匹配搜索数组中指定元素出现的第一个的位置,未出现返回false
			//array_search($real_path,$this->dirs)
			//array_count_values 统计数组中各个元素出现的个数
	}

	public function ByStrChr($dir){
		if(is_dir($dir)){
				$type="dir";
				 $this->getrealpath($dir,$type);
		}
		if(is_file($dir)){
				$type="file";
				$this->getrealpath($dir,$type);
		}
	}
	
	public function start($dir){
		// 扫描路劲 scandir 这个函数不太安全
		$resources = scandir($dir);
		foreach($resources as $k => $res){
			if ( $res == "." || $res == ".." ){
				continue;
			}
			$res = $dir.DIRECTORY_SEPARATOR.$res;
			$this->ByStrChr($res);
		}
   	}
   }
	
	$file = new file();
	$dir = '/tmp';
	$file->start($dir);
	var_dump($file->getFiles());
	var_dump($file->getDirs());
?>
