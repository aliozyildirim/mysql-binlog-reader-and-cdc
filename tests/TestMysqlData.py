import unittest
import time
import json

from mysqlBinlogReader import insert_database, read_last_pos, save_update_data, data_handler


class insertDatabaseTestCase(unittest.TestCase):

    def test_save_crm_updates(self):
        jsonRow = json.dumps({"table": "update_test_data",
                              "row":
                                  {"before_values":
                                       {"STATUS": 1, "PRODUCT_ID": 448732, "PRICE_ALT": 139.9},
                                   "after_values": {"STATUS": 7, "PRODUCT_ID": 448732, "PRICE_ALT": 139.9}},
                              "type": "UpdateRowsEvent",
                              "schema": "besiktas"
                              })

        self.assertTrue(save_update_data(jsonRow), 'Ok')

    def test_insert(self):
        str_now = time.strftime('%Y-%m-%d %H:%M:%S')

        sqlCdc = "INSERT INTO update_data (table_name, current_id, method, updated_at, inserted_at ,before_values, after_values, database_d) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        valCdc = (str('besiktas'), 1903, str('Insert'), str_now, str_now, 'Null',
                  str({"STATUS": 7, "PRODUCT_ID": 535278, "PRICE_ALT": 85.9}), str('besiktas'))

        self.assertTrue(insert_database(sqlCdc, valCdc), 'Ok')

    def test_update(self):
        str_now = time.strftime('%Y-%m-%d %H:%M:%S')

        sqlCdc = "INSERT INTO update_data (table_name, current_id, method, updated_at, inserted_at ,before_values, after_values, database_d) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        valCdc = (str('besiktas'), 1903, str('Update'), str_now, str_now,
                  str({"STATUS": 7, "PRODUCT_ID": 535278, "PRICE_ALT": 85.2}),
                  str({"STATUS": 7, "PRODUCT_ID": 535278, "PRICE_ALT": 85.9}), str('besiktas'))

        self.assertTrue(insert_database(sqlCdc, valCdc), 'Ok')

    def test_read_last_pos(self):
        self.assertTrue(read_last_pos(), 'Ok')


if __name__ \
        == '__main__':
    unittest.main()
