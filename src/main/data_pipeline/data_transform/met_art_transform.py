import pandas as pd
from src.main.data_pipeline.data_transform.dimension_extractor import DimensionExtractor
import logging


class MetArtTransform:
    # Input Conditions
    DIMENSIONS_RAW_DATA_FIELD = "Dimensions"
    ART_ID = "Object ID"

    # Output Details
    DIMENSION_OUTPUT_FIELDS = ["Length", "Width", "Height"]

    # # Cleaning Details
    # No Dimensions
    NONE_DIMENSIONS_FLAGS = ["Dimensions unavailable"]

    DEFAULT_EMPTY_VALUE = 0

    def __init__(self):
        self.dimension_extractor = DimensionExtractor()

    def __check_known_no_dimensions(self, dimensions_raw: str):
        return dimensions_raw in self.NONE_DIMENSIONS_FLAGS

    def __assign_empty_dimensions_placeholders(self, data: pd.DataFrame) -> None:
        for field in self.DIMENSION_OUTPUT_FIELDS:
            data.loc[:, field] = self.DEFAULT_EMPTY_VALUE

    def __extract_data(self, raw_data: str) -> list:
        cleaned_dimensions = self.dimension_extractor.extractation(raw_data)
        return [cleaned_dimensions.get(field, self.DEFAULT_EMPTY_VALUE) for field in self.DIMENSION_OUTPUT_FIELDS]

    def execute(self, art_data: pd.DataFrame) -> pd.DataFrame:

        self.__assign_empty_dimensions_placeholders(art_data)

        for index, row in art_data.iterrows():
            if self.__check_known_no_dimensions(row[self.DIMENSIONS_RAW_DATA_FIELD]):
                logging.info("%s has been flagged as no dimensions found.", row[self.ART_ID])
                continue
            art_data.loc[index, self.DIMENSION_OUTPUT_FIELDS] = self.__extract_data(row[self.DIMENSIONS_RAW_DATA_FIELD])
        return art_data[[self.ART_ID, self.DIMENSIONS_RAW_DATA_FIELD, *self.DIMENSION_OUTPUT_FIELDS]]
