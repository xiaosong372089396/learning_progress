#!/usr/bin/env python
# -\*-coding: utf-8-\*-

''' 建表语句
CREATE TABLE IF NOT EXISTS `mytable1`(
   `id` INT UNSIGNED AUTO_INCREMENT,
   `myname` VARCHAR(10) NOT NULL,
   PRIMARY KEY ( `id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
'''

# insert into mytable1 (myname) values ("xianyu1"),("xianyu2");\
# insert into mytable1 (myname) values ("xianyu1"),("xianyu2");\
# delete from mytable1 where id=1; \
import MySQLdb

def table_structure(mysql_structure):
    # 待审核/执行的sql语句（需包含目标数据库的地址、端口 等参数）--enable-check 检测SQL语句但不执行，和--enable-execute的区别
    sql1 = '/* --user=root;--password=123.com;--host=192.168.10.73;--port=3306;--enable-execute; */\
    inception_magic_start;\
    use inc_test;'
    sql2 = 'inception_magic_commit;'
    sql = sql1 + mysql_structure + sql2
    try:
        conn = MySQLdb.connect(host='192.168.10.73', user='inception', passwd='inception', db='inception', port=6669, use_unicode=True, charset="utf8")  # inception的地址、端口等
        cur = conn.cursor()
        ret = cur.execute(sql)
        result = cur.fetchall()
        num_fields = len(cur.description)
        field_names = [i[0] for i in cur.description]
        print result
        '''
        for row in result:
            print row[0], "|",row[1],"|",row[2],"|",row[3],"|",row[4],"|",
            row[5],"|",row[6],"|",row[7],"|",row[8],"|",row[9],"|",row[10]
        '''
        cur.close()
        conn.close()
    except MySQLdb.Error, e:
         print "Mysql Error %d: %s" % (e.args[0], e.args[1])

