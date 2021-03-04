import unittest
from src.main.data_pipeline.data_transform.met_art_transform import MetArtTransform
import pandas as pd
from pandas.testing import assert_frame_equal


class TestExecute(unittest.TestCase):

    def setUp(self) -> None:
        self.transformer = MetArtTransform()

    def test_no_dimension_data(self):
        df_test = pd.DataFrame({'Object ID': {0: 1},
                                'Dimensions': {0: 'Dimensions unavailable'}})
        df_output_true = pd.DataFrame({'Object ID': {0: 1},
                                       'Dimensions': {0: 'Dimensions unavailable'},
                                       'Length': {0: 0.0}, 'Width': {0: 0.0}, 'Height': {0: 0.0}})
        df_output = self.transformer.execute(df_test)
        print(df_output)
        assert_frame_equal(df_output_true, df_output)

    def test_dimensions_data(self):
        df_test = pd.DataFrame({'Object ID': {0: 1},
                                'Dimensions': {0: 'H. 6 3/4 in. (17.1 cm); Diam. 3 3/8 in. (8.6 cm)'}})
        df_output_true = pd.DataFrame({'Object ID': {0: 1},
                                       'Dimensions': {0: 'H. 6 3/4 in. (17.1 cm); Diam. 3 3/8 in. (8.6 cm)'},
                                       'Length': {0: 8.6}, 'Width': {0: 8.6}, 'Height': {0: 17.1}})
        df_output = self.transformer.execute(df_test)
        assert_frame_equal(df_output_true, df_output)


if __name__ == '__main__':
    unittest.main()
