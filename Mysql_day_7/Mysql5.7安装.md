###  CentOS7安装Mysql



```
#创建运行MySQL的账号
[root@mysql ~]# useradd mysql -s /sbin/nologin
[root@mysql ~]# id mysql
uid=1001(mysql) gid=1001(mysql) 组=1001(mysql)


#创建mysql相关目录
[root@mysql ~]# mkdir -p /data/mysql/mysql3306/{conf,data,logs,tmp}
[root@mysql ~]# chown -R mysql.mysql /data/mysql/

#解压mysql安装文件到/usr/local下
[root@mysql ~]# tar xf mysql-5.7.20-linux-glibc2.12-x86_64.tar.gz  -C /usr/local/
[root@mysql ~]# ln -sv /usr/local/mysql-5.7.20-linux-glibc2.12-x86_64 /usr/local/mysql
"/usr/local/mysql" -> "/usr/local/mysql-5.7.20-linux-glibc2.12-x86_64"


#创建mysql配置文件
[root@mysql ~]# cat /data/mysql/mysql3306/conf/my.cnf
[client]
port            = 3306
socket          = /tmp/mysql3306.sock

[mysql]
prompt="\\u@\\h [\\d]>"
#pager="less -i -n -S"
#tee=/opt/mysql/query.log
no-auto-rehash

[mysqld]
#misc
user = mysql
basedir = /usr/local/mysql
datadir = /data/mysql/mysql3306/data
port = 3306
socket = /tmp/mysql3306.sock
event_scheduler = 0

tmpdir = /data/mysql/mysql3306/tmp
#timeout
interactive_timeout = 300
wait_timeout = 300

#character set
character-set-server = utf8

open_files_limit = 65535
max_connections = 100
max_connect_errors = 100000
lower_case_table_names =1

#
explicit_defaults_for_timestamp=1

#symi replication

#rpl_semi_sync_master_enabled=1
#rpl_semi_sync_master_timeout=1000 # 1 second
#rpl_semi_sync_slave_enabled=1

#logs
log-output=file
slow_query_log = 1
slow_query_log_file = slow.log
log-error = error.log
pid-file = mysql.pid
long_query_time = 1
#log-slow-admin-statements = 1
#log-queries-not-using-indexes = 1
log-slow-slave-statements = 1

#binlog
#binlog_format = STATEMENT
binlog_format = row
server-id = 1013306
log-bin = /data/mysql/mysql3306/logs/mysql-bin
binlog_cache_size = 1M
max_binlog_size = 256M
sync_binlog = 0
expire_logs_days = 10
#procedure
log_bin_trust_function_creators=1

#
gtid-mode = on
enforce-gtid-consistency=1


#relay log
skip_slave_start = 1
max_relay_log_size = 128M
relay_log_purge = 1
relay_log_recovery = 1
relay-log=relay-bin
relay-log-index=relay-bin.index
log_slave_updates
#slave-skip-errors=1032,1053,1062
#skip-grant-tables

#buffers & cache
table_open_cache = 2048
table_definition_cache = 2048
table_open_cache = 2048
max_heap_table_size = 96M
sort_buffer_size = 128K
join_buffer_size = 128K
thread_cache_size = 200
query_cache_size = 0
query_cache_type = 0
query_cache_limit = 256K
query_cache_min_res_unit = 512
thread_stack = 192K
tmp_table_size = 96M
key_buffer_size = 8M
read_buffer_size = 2M
read_rnd_buffer_size = 16M
bulk_insert_buffer_size = 32M

#myisam
myisam_sort_buffer_size = 128M
myisam_max_sort_file_size = 10G
myisam_repair_threads = 1

#innodb
innodb_buffer_pool_size = 100M
innodb_buffer_pool_instances = 1
innodb_data_file_path = ibdata1:100M:autoextend
innodb_flush_log_at_trx_commit = 2
innodb_log_buffer_size = 8M
innodb_log_file_size = 100M
innodb_log_files_in_group = 3
innodb_max_dirty_pages_pct = 50
innodb_file_per_table = 1
innodb_rollback_on_timeout
innodb_status_file = 1
innodb_io_capacity = 2000
transaction_isolation = READ-COMMITTED
innodb_flush_method = O_DIRECT

loose_tokudb_cache_size=100M
loose_tokudb_directio=ON
loose_tokudb_fsync_log_period=1000
loose_tokudb_commit_sync=0

#初始化Mysql
[root@mysql ~]# /usr/local/mysql/bin/mysqld --defaults-file=/data/mysql/mysql3306/conf/my.cnf --initialize

#获取初始化生成的密码
[root@mysql ~]# cat /data/mysql/mysql3306/data/error.log | grep password | awk '{print $NF}'
H=?ycalZA4.e


#启动MySQL
[root@mysql ~]# /usr/local/mysql-5.7.20-linux-glibc2.12-x86_64/bin/mysqld --defaults-file=/data/mysql/mysql3306/conf/my.cnf &
[1] 4596
[root@mysql ~]# ss -tnl
State      Recv-Q Send-Q                                                                        Local Address:Port                                                                          Peer Address:Port
LISTEN     0      128                                                                                       *:22                                                                                       *:*
LISTEN     0      100                                                                               127.0.0.1:25                                                                                       *:*
LISTEN     0      70                                                                                       :::3306                                                                                    :::*
LISTEN     0      128                                                                                      :::22                                                                                      :::*
LISTEN     0      100                                                                                     ::1:25                                                                                      :::*
[root@mysql ~]# ps aux |grep mysql
mysql     4596  3.8 17.8 1077724 181116 pts/0  Sl   04:01   0:00 /usr/local/mysql-5.7.20-linux-glibc2.12-x86_64/bin/mysqld --defaults-file=/data/mysql/mysql3306/conf/my.cnf
root      4632  0.0  0.0 112656   972 pts/0    R+   04:01   0:00 grep --color=auto mysql


#连接到数据库
[root@mysql ~]# /usr/local/mysql/bin/mysql -u root -p -S /tmp/mysql3306.sock
Enter password:                         #这输入的是上文中获取到的密码
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 4
Server version: 5.7.20-log

Copyright (c) 2000, 2017, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.


#第一次操作室要求修改密码
mysql> show databases;          
ERROR 1820 (HY000): You must reset your password using ALTER USER statement before executing this statement.

#修改root用户的密码为123456
mysql> alter user user() identified by '123456';
Query OK, 0 rows affected (0.00 sec)

mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
4 rows in set (0.00 sec)




#用新密码重新登陆
[root@mysql ~]# /usr/local/mysql/bin/mysql -u root -p123456 -S /tmp/mysql3306.sock
mysql: [Warning] Using a password on the command line interface can be insecure.
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 5
Server version: 5.7.20-log MySQL Community Server (GPL)

Copyright (c) 2000, 2017, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql>



```
### 关闭Mysql数据库

```
[root@mysql ~]# ps aux |grep mysql |grep -v grep
mysql     4596  0.1 17.8 1077924 181364 pts/0  Sl   04:01   0:00 /usr/local/mysql-5.7.20-linux-glibc2.12-x86_64/bin/mysqld --defaults-file=/data/mysql/mysql3306/conf/my.cnf
[root@mysql ~]# ss -tnl |grep 3306
LISTEN     0      70                       :::3306                    :::*


#通过mysqladmin接口关闭数据库
[root@mysql ~]# /usr/local/mysql/bin/mysqladmin -u root -p123456 -S /tmp/mysql3306.sock shutdown
mysqladmin: [Warning] Using a password on the command line interface can be insecure.

#检查结果
[root@mysql ~]# ss -tnl |grep 3306
[root@mysql ~]# ps aux |grep mysql |grep -v grep
```
