import re
import logging


class DimensionExtractor:
    """

    Works to split the raw dimensions string into the following output:

    Units in cm.

    -> ["art_length", "art_width", "art_height"]

       Example:

       "Diam. 2 5/8 × 1/4 in., 0.3 lb. (6.7 × 0.6 cm, 0.1 kg)"
        -> {'art_length': 27, 'art_width': 22.5}


    """

    DEFAULT_MEASUREMENT_DIRECTIONS = ["art_length", "art_width", "art_height"]

    # Data with multi fields commonly split by:
    DIMENSION_SPLITS = [";", "\r\n", "mount:", "frame:", "\n", "confirmed:", "Forks", "sheet:"]
    MULTI_DIMENSIONS_SPLIT = ["x", "×", "-", ","]
    OVERALL_FLAG = "overall:"

    # Identify direction of measurement
    MEASUREMENT_DIRECTIONS_BY_FLAGS = {"h.": ["art_height"], "h x": ["art_height"], "h:": ["art_height"],
                                       "h>": ["art_height"], "height:": ["art_height"], " h ": ["art_height"],
                                       "l.": ["art_length"], " L ": ["art_length"], "length:": ["art_width"],
                                       "diam": ["art_length", "art_width"], "d ": ["art_length", "art_width"],
                                       "d.": ["art_length", "art_width"], "w.": ["art_width"], "th.": ["art_width"],
                                       "width:": ["art_width"], "w:": ["art_width"],
                                       }

    IMPERIAL_UNITS = ["in.", "inches", "inch"]
    METRIC_UNIT = "cm"

    # Regex Match Patterns
    CM_BRACKETS_MATCH = """\((.*cm)"""
    ONLY_TEXT_BRACKETS = """\([a-z|\s]+\)"""
    INBRACKETS_MATCH = """\(.*?\)"""
    WIEGHT_MATCH = """(?<=cm)(.*)(?=g*)"""
    NUMBER_EXTRACT = """\d+\.\d+|\d+"""

    def __init__(self):
        self.search_imperial = re.compile('|'.join(self.IMPERIAL_UNITS))

    def __get_imperial_text(self, text_brackets: list) -> list:
        imperial_brackets = []
        for text in text_brackets:
            if self.METRIC_UNIT not in text:
                imperial_brackets.append(text)
        return imperial_brackets

    def __get_metric_text(self, text_brackets: list) -> list:
        metric_brackets = []
        for text in text_brackets:
            if self.METRIC_UNIT in text:
                metric_brackets.append(re.findall(self.CM_BRACKETS_MATCH, text)[0])
        return "x".join(metric_brackets)

    def __find_cm_data_in_or_out_brackets(self, text_brackets: list, dimensions: str) -> str:
        """Example in brackets:

                dimensions:  '12 1/2 x 7 7/8 in. (31.8 x 20 cm)'
                    -> '31.8 x 20'

           Example imperial in brackets:

                dimensions: l. 5.8 cm (2-5/16 in.) x w. 4.5 cm (1-3/4 in.) x h. 4 cm (1-9/16)
                    -> l. 5.8 cm x w. 4.5 cm x H. 4 cm

           Example no brackets:

                dimensions:  "D 10 cm x H 5.5 cm"
                    -> 'D 10 cm x H 5.5 cm'
                """
        # No brackets
        if not text_brackets:
            # Remove any additional associated weight data.
            weight_info = re.findall(self.WIEGHT_MATCH, dimensions)
            if weight_info and "g" in dimensions:
                return re.sub(weight_info[0], '', dimensions)
            return dimensions

        # Metric data in brackets
        metric_string = self.__get_metric_text(text_brackets)
        if metric_string:
            return metric_string

        # if imperial units in brackets.
        imperial_brackets = self.__get_imperial_text(text_brackets)
        if imperial_brackets:
            return re.sub("|".join(imperial_brackets), '', dimensions).replace("()", "").strip()

    def __extract_cm_data(self, dimensions: str) -> list:

        """
        Example in brackets:

         dimensions:  '12 1/2 x 7 7/8 in. (31.8 x 20 cm)'
                    -> '31.8 x 20' -> [31.8, 20]

        Example imperial in brackets:

        dimensions: l. 5.8 cm (2-5/16 in.) x w. 4.5 cm (1-3/4 in.) x h. 4 cm (1-9/16)
                   -> l. 5.8 cm x w. 4.5 cm x H. 4 cm -> [5.8, 4.5, 4]
        Example no brackets:

        dimensions:  "D 10 cm x H 5.5 cm"
                   -> 'D 10 cm x H 5.5 cm' -> [10, 5.5]
        """

        in_brackets_text = re.findall(self.INBRACKETS_MATCH, dimensions)
        cm_extracted = self.__find_cm_data_in_or_out_brackets(in_brackets_text, dimensions)


        cm_extracted = re.split("|".join(self.MULTI_DIMENSIONS_SPLIT), cm_extracted)

        clean_extracted = [re.findall(self.NUMBER_EXTRACT, item) for item in cm_extracted]
        return [item[0] for item in clean_extracted if item]

    def __get_direction_id_flags(self, text: str) -> list:
        """

        Get direction flags and order.

        text: "h: 9 7/8 (25.1 cm) x diam. 8 1/4 in.(21 cm)"

        -> ["h:", "diam."]

        """

        flags = []
        order = []
        for key in self.MEASUREMENT_DIRECTIONS_BY_FLAGS.keys():
            if key in text:
                flags.append(key)
                order.append(text.find(key))

        if not flags:
            return flags

        return [x for _, x in sorted(zip(order, flags))]

    def __all_measurement_directions(self, dimensions_split: list) -> bool:
        return len(dimensions_split) == 3

    def __map_cm_data_to_direction_flags(self, measurement_direction_flags: list, cm_data_split: list,
                                         out_dimensions: dict):

        for index, value in enumerate(cm_data_split):
            if measurement_direction_flags:

                # Account for when there are ranged values for the same dimension.
                if index < len(measurement_direction_flags):
                    flag = measurement_direction_flags[index]

                directions = self.MEASUREMENT_DIRECTIONS_BY_FLAGS[flag]
            else:
                # default to direction based on position
                directions = [self.DEFAULT_MEASUREMENT_DIRECTIONS[index]]

            for direction in directions:
                existing_value = out_dimensions.get(direction, "")
                if existing_value:
                    out_dimensions[direction] = max([float(value), existing_value])
                else:
                    out_dimensions[direction] = float(value)

    def __extract_values(self, text: str, out_dimensions: dict) -> None:

        if self.METRIC_UNIT not in text:
            return None

        cm_data_split = self.__extract_cm_data(text)

        if self.__all_measurement_directions(cm_data_split):
            self.__map_cm_data_to_direction_flags([], cm_data_split, out_dimensions)
            return

        # Check for mention of any possible measurement directions
        measurement_direction_flags = self.__get_direction_id_flags(text)

        # Ranged values

        # update the out_dimensions
        self.__map_cm_data_to_direction_flags(measurement_direction_flags, cm_data_split, out_dimensions)

    def __remove_text_only_brackets(self, raw_dimensions: str) -> str:
        """
        Example:
          raw_dimensions:  L. 13 1/2 × Diam. (disk) 1 3/4 in. (34.3 × 4.4 cm)

            ->
            L. 13 1/2 × Diam.  1 3/4 in. (34.3 × 4.4 cm)
        """

        text_in_brackets = re.findall(self.ONLY_TEXT_BRACKETS, raw_dimensions)
        if text_in_brackets:
            return re.sub("|".join(text_in_brackets), '', raw_dimensions).replace("()", "")

        return raw_dimensions

    def extractation(self, raw_dimensions: str) -> dict:

        raw_dimensions = raw_dimensions.lower()

        out_dimensions = {}

        if not isinstance(raw_dimensions, str):
            return out_dimensions

        # Remove any text only brackets.
        raw_dimensions_without_text_brackets = self.__remove_text_only_brackets(raw_dimensions)

        raw_dimensions_split_sets = re.split("|".join(self.DIMENSION_SPLITS), raw_dimensions_without_text_brackets)

        if self.OVERALL_FLAG in raw_dimensions:
            # Only first set of interest.
            self.__extract_values(raw_dimensions_split_sets[0], out_dimensions)
            return out_dimensions
        for raw_dimension in raw_dimensions_split_sets:
            self.__extract_values(raw_dimension, out_dimensions)

        return out_dimensions
