# mysql-binlog-reader-and-cdc
with BinLogStreamReader insert Change Data Capture database..


# MySQL server settings

server-id		 = 100 <br>
log_bin			 = /var/log/mysql/mysql-bin.log <br>
expire_logs_days = 12<br>
max_binlog_size  = 120M <br>
binlog-format    = row<br>

Very important for read, update and delete -- binlog-format = <b><i> row</i> </b>  



# Project Referenced By and Used


Mysql binlog read help  =  https://github.com/noplay/python-mysql-replication