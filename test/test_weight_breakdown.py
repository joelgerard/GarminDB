"""Test weight breakdown import."""

import unittest
import datetime
import logging
import sys

from garmindb import GarminWeightData
from garmindb.garmindb import GarminDb, Weight

# Add the test directory to the path so we can import TestDBBase
sys.path.append('test')
from test_db_base import TestDBBase

logger = logging.getLogger(__name__)

class TestWeightBreakdown(TestDBBase, unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        from garmindb import GarminConnectConfigManager
        gc_config = GarminConnectConfigManager()
        cls.test_db_params = gc_config.get_db_params(test_db=True)
        cls.garmin_db = GarminDb(cls.test_db_params)
        table_dict = {
            'weight_table': Weight
        }
        super().setUpClass(cls.garmin_db, table_dict, table_can_be_empty=['weight_table'])

    def test_weight_breakdown_import(self):
        # Mock JSON data from Garmin
        json_data = {
            'startDate': datetime.datetime(2024, 1, 1),
            'dateWeightList': [
                {
                    'weight': 80000, # 80kg in grams
                    'bmi': 24.5,
                    'bodyFat': 18.2,
                    'bodyWater': 60.1,
                    'boneMass': 3500, # 3.5kg in grams
                    'muscleMass': 40000, # 40kg in grams
                    'visceralFat': 5
                }
            ]
        }

        # Create importer with metric system
        import fitfile
        measurement_system = fitfile.field_enums.DisplayMeasure.metric
        import tempfile
        with tempfile.TemporaryDirectory() as temp_dir:
            importer = GarminWeightData(self.test_db_params, temp_dir, False, measurement_system, 0)
        importer.garmin_db = self.garmin_db # Use our test db

        # Process the mocked JSON
        result = importer._process_json(json_data)
        self.assertEqual(result, 1)

        # Verify the data in the database
        with self.garmin_db.managed_session() as session:
            rows = session.query(Weight).all()
            self.assertEqual(len(rows), 1)
            row = rows[0]
            self.assertEqual(row.day, datetime.date(2024, 1, 1))
            self.assertEqual(row.weight, 80.0)
            self.assertEqual(row.bmi, 24.5)
            self.assertEqual(row.body_fat, 18.2)
            self.assertEqual(row.body_water, 60.1)
            self.assertEqual(row.bone_mass, 3.5)
            self.assertEqual(row.muscle_mass, 40.0)
            self.assertEqual(row.visceral_fat, 5)

    def test_weight_breakdown_import_statute(self):
        # Test with statute system (lbs)
        json_data = {
            'startDate': datetime.datetime(2024, 1, 2),
            'dateWeightList': [
                {
                    'weight': 80000, # 80kg in grams
                    'bmi': 24.5,
                    'bodyFat': 18.2,
                    'bodyWater': 60.1,
                    'boneMass': 3500, # 3.5kg in grams
                    'muscleMass': 40000, # 40kg in grams
                    'visceralFat': 5
                }
            ]
        }

        import fitfile
        measurement_system = fitfile.field_enums.DisplayMeasure.statute
        import tempfile
        with tempfile.TemporaryDirectory() as temp_dir:
            importer = GarminWeightData(self.test_db_params, temp_dir, False, measurement_system, 0)
        importer.garmin_db = self.garmin_db

        result = importer._process_json(json_data)
        self.assertEqual(result, 1)

        with self.garmin_db.managed_session() as session:
            row = session.query(Weight).filter(Weight.day == datetime.date(2024, 1, 2)).one()
            # 80kg is approx 176.37 lbs
            self.assertAlmostEqual(row.weight, 176.37, places=1)
            # Bone mass: 3.5kg is approx 7.7 lbs
            self.assertAlmostEqual(row.bone_mass, 7.7, places=1)
            # Muscle mass: 40kg is approx 88.18 lbs
            self.assertAlmostEqual(row.muscle_mass, 88.2, places=1)

if __name__ == '__main__':
    unittest.main()
