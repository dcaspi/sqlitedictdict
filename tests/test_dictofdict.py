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
        self.assertEqual(set(self.d["mydict"].items()), {("a", 1), ("b", 2), ("c", "d")})

    def test_partial(self):
        first_dict = {"a": 1, "b": 2, "c": "d"}
        second_dict = {"a": 2, "c": "e", "f": "g"}
        self.d["first_dict"] = first_dict
        self.d["second_dict"] = second_dict

        self.assertEqual(self.d["first_dict"], first_dict)
