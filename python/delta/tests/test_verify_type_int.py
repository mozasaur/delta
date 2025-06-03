import sys
import types
import importlib
import unittest

class VerifyTypeIntTests(unittest.TestCase):
    def setUp(self) -> None:
        # Stub minimal pyspark modules required for importing delta.tables
        pyspark = types.ModuleType('pyspark')
        pyspark.since = lambda v: (lambda f: f)
        sql = types.ModuleType('pyspark.sql')
        class Column: pass
        class DataFrame: pass
        class SparkSession:
            class Builder: pass
        functions = types.ModuleType('pyspark.sql.functions')
        sql.Column = Column
        sql.DataFrame = DataFrame
        sql.SparkSession = SparkSession
        sql.functions = functions
        sql.types = types.ModuleType('pyspark.sql.types')
        sql.types.DataType = object
        sql.types.StructType = object
        sql.types.StructField = object
        sys.modules['pyspark'] = pyspark
        sys.modules['pyspark.sql'] = sql
        sys.modules['pyspark.sql.functions'] = functions
        sys.modules['pyspark.sql.types'] = sql.types
        sys.modules['pyspark.sql.column'] = types.ModuleType('pyspark.sql.column')
        sys.modules['pyspark.sql.column'].Column = Column
        sys.modules['delta.exceptions'] = types.ModuleType('delta.exceptions')
        self.DeltaTable = importlib.import_module('delta.tables').DeltaTable

    def tearDown(self) -> None:
        modules_to_remove = [m for m in sys.modules.keys() if m.startswith('pyspark') or m == 'delta.exceptions']
        for m in modules_to_remove:
            sys.modules.pop(m, None)

    def test_bool_rejected(self) -> None:
        with self.assertRaises(ValueError):
            self.DeltaTable._verify_type_int(True, 'value')

    def test_int_ok(self) -> None:
        # Should not raise
        self.DeltaTable._verify_type_int(1, 'value')

if __name__ == '__main__':
    unittest.main()
