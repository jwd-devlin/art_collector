import unittest
from src.main.data_pipeline.data_transform.dimension_extractor import DimensionExtractor


class TestExecute(unittest.TestCase):

    def setUp(self) -> None:
        self.extractor = DimensionExtractor()

    def test_two_sets_of_diameters_data(self):
        input_0 = "a: H. 1 3/8 in. (3.5 cm); Diam. 1 5/16 in. (3.3 cm)\r\nb: Diam. 2 in. (5.1 cm)"
        expected = {"art_length": 5.1, "art_width": 5.1, "art_height": 3.5}
        output = self.extractor.extractation(input_0)
        self.assertEqual(expected, output)

    def test_two_measurement_direction_values_no_direction_flags(self):
        input_0 = '12 1/2 x 7 7/8 in. (31.8 x 20 cm)'
        expected = {"art_length": 31.8, "art_width": 20}
        output = self.extractor.extractation(input_0)
        self.assertEqual(expected, output)

    def test_three_measurement_direction_values_no_direction_flags(self):
        input_0 = "34 3/4 x 32 3/8 x 4 in. (88.3 x 82.2 x 10.2 cm)"
        expected = {"art_length": 88.3, "art_width": 82.2, "art_height": 10.2}
        output = self.extractor.extractation(input_0)
        self.assertEqual(expected, output)

    def test_one_value_and_measurement_direction_flag(self):
        input_1 = 'H. 12 3/4 in. (32.4 cm)'
        expected_1 = {"art_height": 32.4}
        output_1 = self.extractor.extractation(input_1)
        self.assertEqual(expected_1, output_1)

        input_2 = "H. 37 1/2 in. (95.3 cm.)"
        expected_2 = {"art_height": 95.3}
        output_2 = self.extractor.extractation(input_2)
        self.assertEqual(expected_2, output_2)

        input_2 = 'Diam. 5 3/4 in. (14.6 cm)'
        expected_2 = {"art_length": 14.6, "art_width": 14.6}
        output_2 = self.extractor.extractation(input_2)
        self.assertEqual(expected_2, output_2)

    def test_overall_with_multi_sets_of_dimension_data(self):
        input_0 = 'Overall: 3 x 6 1/2 in. (7.6 x 16.5 cm); ' \
                  '4 oz. 10 dwt. (140.6 g)\r\nLip: Diam. 4 1/16 in. (10.3 cm)\r\nFoot: Diam. 2 3/4 in. (7 cm)'
        expected = {"art_length": 7.6, "art_width": 16.5}
        output = self.extractor.extractation(input_0)
        self.assertEqual(expected, output)

    def test_different_string_for_direction_split(self):
        input_0 = '24 1/2 in. × 13 in. × 20 3/8 in. (62.2 × 33 × 51.8 cm)'
        expected = {"art_length": 62.2, "art_width": 33.0, "art_height": 51.8}
        output = self.extractor.extractation(input_0)
        self.assertEqual(expected, output)

    def test_different_string_for_direction_split_1(self):
        input_0 = '6 x 4 x 1 in. (15.2 x 10.2 x 2.5 cm)'
        expected = {"art_length": 15.2, "art_width": 10.2, "art_height": 2.5}
        output = self.extractor.extractation(input_0)
        self.assertEqual(expected, output)

    def test_imperial_units_in_brackets(self):
        input_0 = '6 x 4 x 1 in. (15.2 x 10.2 x 2.5 cm)'
        expected = {"art_length": 15.2, "art_width": 10.2, "art_height": 2.5}
        output = self.extractor.extractation(input_0)
        self.assertEqual(expected, output)

    def test_remove_text_in_brackets(self):
        input_0 = 'L. 13 1/2 × Diam. (disk) 1 3/4 in. (34.3 × 4.4 cm)'
        expected = {"art_length": 34.3, "art_width": 4.4}
        output = self.extractor.extractation(input_0)
        self.assertEqual(expected, output)

    def test_multi_cm_brackets(self):
        input_0 = '11 in. (27.9 cm) x 11 1/2 in. (29.2 cm) x 8 1/4 in. (21 cm)'
        expected = {"art_length": 27.9, "art_width": 29.2, "art_height": 21}
        output = self.extractor.extractation(input_0)
        self.assertEqual(expected, output)

    def test_only_cm_and_text_brackets(self):
        input_0 = '6.2 x 10.3 cm (overall)'
        expected = {"art_length": 6.2, "art_width": 10.3}
        output = self.extractor.extractation(input_0)
        self.assertEqual(expected, output)

        input_1 = "14 x 13.9 cm, wt. 87.17 g."
        expected_1 = {"art_length": 14, "art_width": 13.9}
        output_1 = self.extractor.extractation(input_1)
        self.assertEqual(expected_1, output_1)

    def test_imperial_in_brackets(self):
        input_0 = 'L. 18 cm (7 1/16 in.)'
        expected = {"art_length": 18}
        output = self.extractor.extractation(input_0)
        self.assertEqual(expected, output)

    def test_multi_cm_brackets_two_direction_flags(self):
        input_0 = 'H: 9 7/8 (25.1 cm) x Diam. 8 1/4 in.(21 cm)'
        expected = {'art_height': 25.1, 'art_length': 21.0, 'art_width': 21.0}
        output = self.extractor.extractation(input_0)
        self.assertEqual(expected, output)

        input_1 = "L. 19 x W. 1 1/2 inches (48.3 x 3.8 cm)"
        expected_1 = {"art_length": 48.3, "art_width": 3.8}
        output_1 = self.extractor.extractation(input_1)
        self.assertEqual(expected_1, output_1)

    def test_mult_values_two_directions(self):
        input_0 = "D 10 cm x H 5.5 cm"
        expected_0 = {"art_length": 10, "art_width": 10, 'art_height': 5.5}
        output_0 = self.extractor.extractation(input_0)
        self.assertEqual(expected_0, output_0)

    def test_comma_separator(self):
        input_0 = "10 5/8 × 16 3/8 × 8 7/8 in. (27 cm, 22.5 cm)"
        expected = {'art_length': 27, 'art_width': 22.5}
        output = self.extractor.extractation(input_0)
        self.assertEqual(expected, output)

    def test_weight_data(self):
        input_0 = "Overall: 16 7/8 x 9 1/8 x 6 3/8 in., 9.068lb. (42.9 x 23.2 x 16.2 cm, 4113g)"
        expected = {"art_length": 42.9, "art_width": 23.2, "art_height": 16.2}
        output = self.extractor.extractation(input_0)
        self.assertEqual(expected, output)

        input_1 = "6 × 6 5/8 × 2 3/4 in., 1.3 lb. (15.2 × 16.8 × 7 cm, 0.6 kg)"
        expected_1 = {"art_length": 15.2, "art_width": 16.8, "art_height": 7}
        output_1 = self.extractor.extractation(input_1)
        self.assertEqual(expected_1, output_1)

    def text_diam_plus_default_thickness(self):
        input_0 = "Diam. 2 5/8 × 1/4 in., 0.3 lb. (6.7 × 0.6 cm, 0.1 kg)"
        expected = {'art_length': 27, 'art_width': 22.5}
        output = self.extractor.extractation(input_0)
        self.assertEqual(expected, output)

    def test(self):
        input_0 = """Approx. 10.2 x 6.3 cm (4 x 2 1/2 in.)"""
        expected = {'art_length': 27, 'art_width': 22.5}
        output = self.extractor.extractation(input_0)
        self.assertEqual(expected, output)


if __name__ == '__main__':
    unittest.main()
