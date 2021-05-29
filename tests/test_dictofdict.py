import sqlitedict
from test_temp_db import TempSqliteDictTest
from accessories import norm_file


class DictOfDictValueTest(TempSqliteDictTest):
    def setUp(self):
        self.d = sqlitedict.SqliteDict(autocommit=True)

    def tearDown(self):
        self.d.terminate()

    def test_dict(self):
        val = {"a": 1}
        self.d["mydict"] = val
        val["b"] = 2
        self.d["mydict"] = val
        self.assertEqual(self.d["mydict"], val)
        val["c"] = "d"
        self.assertNotEqual(self.d["mydict"], val)
        self.d["mydict"] = val
        self.assertEqual(self.d["mydict"], val)
        val["b"] = 4
        self.d["mydict"] = val
        self.assertEqual(self.d["mydict"], val)

    def test_iter(self):
        self.d["mydict"] = {"a": 1, "b": 2, "c": "d"}
        self.assertEqual(set(self.d["mydict"].keys()), {"a", "b", "c"})
        self.assertEqual(set(self.d["mydict"].values()), {1, 2, "d"})
        self.assertEqual(
            set(self.d["mydict"].items()), {("a", 1), ("b", 2), ("c", "d")}
        )

    def test_partial(self):
        first_dict = {"a": 1, "b": 2, "c": "d"}
        second_dict = {"a": 2, "c": "e", "f": "g"}
        self.d["first_dict"] = first_dict
        self.d["second_dict"] = second_dict

        self.assertEqual(self.d["first_dict"], first_dict)
        self.assertEqual(self.d["second_dict"], second_dict)

    def test_reopen_dict(self):
        db = norm_file("tests/db/sqlitedict-of-dict-db.sqlite")

        test_dict = {"a": 1, "b": 2, "c": "d"}

        with sqlitedict.SqliteDict(filename=db, autocommit=True) as dict_db:
            dict_db["my_dict"] = test_dict
            self.assertEqual(dict_db["my_dict"], test_dict)

        with sqlitedict.SqliteDict(
            filename=db, autocommit=True
        ) as dict_db_reopened:
            self.assertEqual(dict_db_reopened["my_dict"], test_dict)

    def test_multiple_tables_same_db(self):
        db_file = norm_file("tests/db/multiple-tables.sqlite")

        conn = sqlitedict.SqliteMultithread(db_file, autocommit=True)
        with sqlitedict.SqliteDict(
            tablename="tableA", conn=conn
        ) as first_dict, sqlitedict.SqliteDict(
            tablename="tableB", conn=conn
        ) as second_dict:
            first_dict["a"] = {"b": "c", "d": 4}
            first_dict["b"] = {"b": "e", "d": 7}
            second_dict["a"] = {"abc": "def"}
            second_dict["c"] = {"def": ["a", "b", "c"]}

            self.assertEqual(first_dict["a"], {"b": "c", "d": 4})
            self.assertEqual(first_dict["b"], {"b": "e", "d": 7})
            self.assertEqual(second_dict["a"], {"abc": "def"})
            self.assertEqual(second_dict["c"], {"def": ["a", "b", "c"]})

        sqlitedict.SqliteDict.close_conn(conn)
