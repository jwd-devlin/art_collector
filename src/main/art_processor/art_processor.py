from src.main.data_pipeline.storage.art_storage import ArtStorage
import logging


class ArtProccessor:
    DEFAULT_MEASUREMENT_DIRECTIONS = ["art_length", "art_width", "art_height"]

    def __init__(self, art_storage: ArtStorage):
        self.art_storage = art_storage

    def __check_no_dimensions(self, art_dimensions):
        return any(art_dimensions.loc[0, ["art_length", "art_width", "art_height"]].tolist())

    def __check_dimensions(self, dimensions, art_dimensions):
        pass

    def does_it_fit(self, art_object_id: int, dimensions: dict) -> bool:

        art_dimensions = self.art_storage.get_dimensions(art_object_id)

        # No art
        if art_dimensions.emtpy:
            logging.info("No art for this id: %s", art_object_id)
            return False

        # No Dimensions
        if self.___check_no_dimensions(art_dimensions):
            return False
