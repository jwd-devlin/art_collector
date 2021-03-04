import unittest
from src.main.data_pipeline.data_transform.dimension_extractor import DimensionExtractor


class TestExecute(unittest.TestCase):

    def setUp(self) -> None:
        self.extractor = DimensionExtractor()

    def test_two_sets_of_diameters_data(self):
        input_0 = "a: H. 1 3/8 in. (3.5 cm); Diam. 1 5/16 in. (3.3 cm)\r\nb: Diam. 2 in. (5.1 cm)"
        expected = {"Length": 5.1, "Width": 5.1, "Height": 3.5}
        output = self.extractor.extractation(input_0)
        self.assertEqual(expected, output)

    def test_two_measurement_direction_values_no_direction_flags(self):
        input_0 = '12 1/2 x 7 7/8 in. (31.8 x 20 cm)'
        expected = {"Length": 31.8, "Width": 20}
        output = self.extractor.extractation(input_0)
        self.assertEqual(expected, output)

    def test_three_measurement_direction_values_no_direction_flags(self):
        input_0 = "34 3/4 x 32 3/8 x 4 in. (88.3 x 82.2 x 10.2 cm)"
        expected = {"Length": 88.3, "Width": 82.2, "Height": 10.2}
        output = self.extractor.extractation(input_0)
        self.assertEqual(expected, output)

    def test_one_value_and_measurement_direction_flag(self):
        input_1 = 'H. 12 3/4 in. (32.4 cm)'
        expected_1 = {"Height": 32.4}
        output_1 = self.extractor.extractation(input_1)
        self.assertEqual(expected_1, output_1)

        input_2 = 'Diam. 5 3/4 in. (14.6 cm)'
        expected_2 = {"Length": 14.6, "Width": 14.6}
        output_2 = self.extractor.extractation(input_2)
        self.assertEqual(expected_2, output_2)

    def test_overall_with_multi_sets_of_dimension_data(self):
        input_0 = 'Overall: 3 x 6 1/2 in. (7.6 x 16.5 cm); ' \
                  '4 oz. 10 dwt. (140.6 g)\r\nLip: Diam. 4 1/16 in. (10.3 cm)\r\nFoot: Diam. 2 3/4 in. (7 cm)'
        expected = {"Length": 7.6, "Width": 16.5}
        output = self.extractor.extractation(input_0)
        self.assertEqual(expected, output)

if __name__ == '__main__':
    unittest.main()