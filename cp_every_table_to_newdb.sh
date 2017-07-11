#! /usr/bin/env bash
# 导出全库的各表的前50条数据
db_host=localhost
db_user=yjy_bak
conn=_
db_password=YJy@back123
cur_time=`date +%Y%m%d%H%M%S`
old_db=yjy_xiyizonghe
new_db=test_xz
back_dir=/www/backup/$new_db
if [ ! -d $back_dir ];then
	mkdir $back_dir
fi

# 导出原有数据库的每一张表
dump_every_table(){
	cd $back_dir
	rm -rf ./*
	tables=`mysql -u$db_user -p$db_password -h $db_host -e "show tables;" $old_db`
	for table in ${tables[@]}
	do
		if [[ ! $table =~ 'Table' ]];then
			mysqldump -u$db_user -p$db_password  $old_db $table --default-character-set=utf8  > ./$cur_time$conn$old_db$conn$table.sql
			echo "正在备份数据" $old_db "中的 "$table "表"
		fi
	done
}

# 复制(导入)到新的db
cp_to_new_db(){
	# 先创建数据库
	mysql -e "create database if not exists $new_db " -u$db_user -p$db_password
	cd $back_dir
	s_f=`ls`
	for t in $s_f
	do
		mysql --database=$new_db -u$db_user -p$db_password < $t
	done 
	rm -rf ./*.sql
}

dump_every_table
cp_to_new_db
