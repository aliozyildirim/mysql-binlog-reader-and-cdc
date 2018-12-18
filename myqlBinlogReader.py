#           ! BESIKTAS !
#        .---.        .-----------
#       /     \  __  /    ------
#      / /     \(  )/    -----
#     //////   ' \/ `   ---
#    //// / // :    : ---
#   // /   /  /`    '--
#  //          //..\\
#         ====UU====UU====
#             '//||\\`
#               ''``

import mysql.connector
import json
import time
from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.row_event import (
    DeleteRowsEvent,
    UpdateRowsEvent,
    WriteRowsEvent,
)


# Change Data Capture Connector
def mysql_conn_cdc():
    db = mysql.connector.connect(
        host="HOST",
        user="USER",
        passwd="PWD",
        database="DBNAME"
    )
    return db


# Change Data Capture Insert Database
def insert_database(sql, val):
    db = mysql_conn_cdc()

    try:
        statement = db.cursor()
        statement.execute(sql, val)

        db.commit()
    except mysql.connector.Error as err:
        print("Ooopss there is have a problem: {}".format(err))


# Please look database.txt
# Save update data sent to insert_database function
def save_update_data(jsonRow, log_file, log_pos):
    # Now date time
    str_now = time.strftime('%Y-%m-%d %H:%M:%S')
    data = json.loads(jsonRow)
    if data['type'] == "UpdateRowsEvent":
        values = json.dumps(data['row']['after_values'], default=data_handler())
        if 'id' in data['row']['after_values']:
            value_id = data['row']['after_values']['id']
        else:
            value_id = 'Null'
        before_values = json.dumps(data['row']['before_values'], default=data_handler)
        method = 'Update'
    elif data['type'] == "DeleteRowsEvent":
        before_values = json.dumps(data['row']['values'], default=data_handler)
        if 'id' in data['row']['values']:
            value_id = data['row']['values']['id']
        else:
            value_id = 'Null'
        method = 'Delete'
        values = None
    else:
        values = json.dumps(data['row']['values'], default=data_handler)
        value_id = data['row']['values']['id']
        before_values = None
        method = 'Insert'

    sqlCdc = "INSERT INTO update_data (table_name, current_id, method, updated_at, inserted_at ,before_values, after_values, database_d, log_file, log_pos) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    valCdc = (str(data['table']), value_id, method, str_now, str_now, str(before_values), str(values), str(data['schema']), str(log_file), log_pos)

    insert_database(sqlCdc, valCdc)

def data_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    elif type(obj).__name__ == 'Decimal':
        return float(obj)
    else:
        raise TypeError(
            "Unserializable object {} of type {}".format(obj, type(obj))
        )

def read_last_pos():
    try:
        db = mysql_conn_cdc()

        statement = db.cursor()
        statement.execute("SELECT * FROM mysql_bin_log_datas ORDER BY id DESC LIMIT 1")

        resultData = statement.fetchone()
        if resultData:
            return resultData[1], int(resultData[2]), True
        else:
            return None, None, False
    except TypeError:
        return None, None, False


def main():
    # last post file, last post id , only first data when starting
    stream_log_file, stream_log_pos, resume_stream_data = read_last_pos()
    # Log db read config information
    stream = BinLogStreamReader(
        connection_settings={
            "host": "HOST",
            "port": 'PORT',
            "user": "USER",
            "passwd": "PWD"},
        log_file=stream_log_file,
        log_pos=stream_log_pos,
        server_id=100,
        resume_stream=resume_stream_data,
        only_events=[DeleteRowsEvent, WriteRowsEvent, UpdateRowsEvent])

    for binlogevent in stream:
        if table_permission_list(binlogevent.table):
            for row in binlogevent.rows:
                event = {
                    "schema": binlogevent.schema,
                    "table": binlogevent.table,
                    "type": type(binlogevent).__name__,
                    "row": row
                }
                jsonRow = json.dumps(event, default=data_handler)

                try:
                    save_update_data(jsonRow, stream.log_file, stream.log_pos)
                except Exception, e:
                    print e


# Table permission list
def table_permission_list(tablename):
    table_list = [
        'test4'
    ]
    if tablename in str(table_list):
        return True
    else:
        return False


if __name__ == "__main__":
    main()
