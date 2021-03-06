import re
import logging


class DimensionExtractor:
    """

    Works to split the raw dimensions string into the following output:

    Units in cm.

    -> [length, width, height]

       'H. 9 in. (22.9 cm); Diam. 3 7/8 in. (9.8 cm)' -> [9.8, 9.8, 22.9 ]
       'L. 26 in. (66 cm)' -> [66, None, None]
       'H. 12 3/4 in. (32.4 cm)' -> [None, None, 32.4]
       'Diam. 5 3/4 in. (14.6 cm)' -> [14.6, 14.6, None]
       'Overall: 4 11/16 x 12 1/2 x 7 1/8 in. (11.9 x 31.8 x 18.1 cm); ...' -> [11.9, 31.8, 18.1]


    """

    DEFAULT_MEASUREMENT_DIRECTIONS = ["art_length", "art_width", "art_height"]
    # Data with multi fields commonly split by:
    DIMENSION_SPLITS = [";", "\r\n", ":"]
    MULTI_DIMENSIONS_SPLIT = ["x", "×"]

    POS_ID_HEIGHT_FLAG = "H. "
    POS_ID_LENGTH_FLAG = "L. "
    POS_ID_DIAMETER_FLAG = "Diam"
    MEASUREMENT_DIRECTIONS_BY_FLAGS = {"H. ": ["art_height"], "L. ": ["art_length"],
                                       "Diam": ["art_length", "art_width"]}

    OVERALL_FLAG = "Overall:"

    METRIC_UNIT = "cm"
    INBRACKETS_MATCH = """\((.*cm)"""

    def __extract_cm_data(self, dimensions: str) -> list:

        """
        Example:
        '12 1/2 x 7 7/8 in. (31.8 x 20 cm)' -> '31.8 x 20' -> [31.8, 20]
        """

        set_extracted = re.findall(self.INBRACKETS_MATCH, dimensions)

        if len(set_extracted) > 1:
            logging.warning(" more DIMENSION_SPLITS found for : %s, Only taking the first.", dimensions)

        clean_extracted = re.sub(self.METRIC_UNIT, '', set_extracted[0]).strip()
        try:
            re.split("|".join(self.MULTI_DIMENSIONS_SPLIT), clean_extracted)
        except:
            print(dimensions)

        return re.split("|".join(self.MULTI_DIMENSIONS_SPLIT), clean_extracted)

    def __get_direction_id_flag(self, text: str) -> str:
        for key in self.MEASUREMENT_DIRECTIONS_BY_FLAGS.keys():
            if key in text:
                return key
        return ""

    def __all_measurement_directions(self, dimensions_split: list) -> bool:
        return len(dimensions_split) == 3

    def __has_diameter_flag(self, positions_flags:str) -> bool:
        return self.POS_ID_DIAMETER_FLAG in positions_flags

    def __get_measurement_directions(self, flag: str, number_dimension_values: int) -> list:
        """

        Returns the possible measurement directions: ["art_length", "art_width", "art_height"]

        Example 1.:
            flag = ""
            number_dimension_values = 3
              -> ["art_length", "art_width", "art_height"]

        Example 2:
            flag = ""
            number_dimension_values = 2
              -> ["art_length", "art_width"]

        Example 2:
            flag = "H"
            number_dimension_values = 1
              -> ["art_height"]
        """
        measurement_directions = self.MEASUREMENT_DIRECTIONS_BY_FLAGS.get(flag, self.DEFAULT_MEASUREMENT_DIRECTIONS)
        return measurement_directions[0:number_dimension_values]

    def __update_out_dimensions_by_order(self, split_dimensions: list, out_dimensions: dict,
                                         measurement_direction_flag: str = "") -> None:
        """
        Example 1:
        Empty out dimensions, simple fill in:

        out_dimensions = {}
        split_dimensions = [97.2, 56.5,52.7]
        measurement_directions = "Diam"

        -> {"art_length":97.2, "art_width": 56.5, "art_height": 52.7}

        Example 2:
        Existing data, pick largest value
        out_dimensions = {"art_length":20, "art_width": 20, "art_height": 52.7}
        split_dimensions = [97.2, 56.5, 52.7]
        measurement_direction_flags = ""

        ->

        """

        measurement_directions = self.__get_measurement_directions(measurement_direction_flag, len(split_dimensions))

        for index, flag in enumerate(measurement_directions):
            if flag not in out_dimensions.keys():
                out_dimensions[flag] = float(split_dimensions[index])
                continue
            existing_value = out_dimensions[flag]
            out_dimensions[flag] = max([float(split_dimensions[index]), existing_value])

    def __extract_values(self, text: str, out_dimensions: dict) -> None:

        if self.METRIC_UNIT not in text:
            return None

        cm_data_split = self.__extract_cm_data(text)

        if self.__all_measurement_directions(cm_data_split):
            self.__update_out_dimensions_by_order(cm_data_split, out_dimensions, "")

        # Check for mention of any possible measurement directions
        measurement_direction_flag = self.__get_direction_id_flag(text)

        # Speacial case for diameter
        if self.__has_diameter_flag(measurement_direction_flag):
            # for diameter translated to length and width required two dimensions
            cm_data_split = cm_data_split * 2


        self.__update_out_dimensions_by_order(cm_data_split, out_dimensions,
                                              measurement_direction_flag)

    def extractation(self, raw_dimensions: str) -> dict:

        out_dimensions = {}

        if not isinstance(raw_dimensions, str):
            print(raw_dimensions)
            return out_dimensions

        raw_dimensions_split_sets = re.split("|".join(self.DIMENSION_SPLITS), raw_dimensions)

        if self.OVERALL_FLAG in raw_dimensions:
            # Only first set of interest.
            self.__extract_values(raw_dimensions_split_sets[0], out_dimensions)
            return out_dimensions
        for raw_dimension in raw_dimensions_split_sets:
            self.__extract_values(raw_dimension, out_dimensions)

        return out_dimensions




