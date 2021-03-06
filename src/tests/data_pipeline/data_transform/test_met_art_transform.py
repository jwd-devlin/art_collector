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
        df_output_true = pd.DataFrame({'object_id': {0: 1},
                                       'dimensions': {0: 'Dimensions unavailable'},
                                       'art_length': {0: 0.0}, 'art_width': {0: 0.0}, 'art_height': {0: 0.0}})
        df_output = self.transformer.execute(df_test)
        print(df_output)
        assert_frame_equal(df_output_true, df_output)

    def test_dimensions_data(self):
        df_test = pd.DataFrame({'Object ID': {0: 1},
                                'Dimensions': {0: 'H. 6 3/4 in. (17.1 cm); Diam. 3 3/8 in. (8.6 cm)'}})
        df_output_true = pd.DataFrame({'object_id': {0: 1},
                                       'dimensions': {0: 'H. 6 3/4 in. (17.1 cm); Diam. 3 3/8 in. (8.6 cm)'},
                                       'art_length': {0: 8.6}, 'art_width': {0: 8.6}, 'art_height': {0: 17.1}})
        df_output = self.transformer.execute(df_test)
        assert_frame_equal(df_output_true, df_output)


if __name__ == '__main__':
    unittest.main()
