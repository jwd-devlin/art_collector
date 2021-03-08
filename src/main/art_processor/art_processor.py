from src.main.data_pipeline.storage.art_storage import ArtStorage
import logging


class ArtProcessor:
    DEFAULT_MEASUREMENT_DIRECTIONS = ["art_length", "art_width", "art_height"]

    def __init__(self, art_storage: ArtStorage):
        self.art_storage = art_storage

    def __check_dimensions(self, art_dimensions: dict, dimensions_user: dict) -> bool:
        for key, value in art_dimensions.items():
            if value > dimensions_user[key]:
                return False
        return True

    def __does_it_fit_python(self, art_object_id: int, dimensions_user: dict) -> bool:
        art_dimensions = self.art_storage.read_dimensions_by_object_id(art_object_id)

        # No art
        if art_dimensions.empty:
            logging.info("No art for this id: %s", art_object_id)
            return False

        return self.__check_dimensions(art_dimensions.loc[0, self.DEFAULT_MEASUREMENT_DIRECTIONS].to_dict(),
                                       dimensions_user)

    def does_it_fit(self, art_object_id: int, dimensions_user: dict, python: bool = True) -> bool:

        if python:
            return self.__does_it_fit_python(art_object_id, dimensions_user)

        dimensions_user_ordered = [dimensions_user[key] for key in self.DEFAULT_MEASUREMENT_DIRECTIONS]
        return self.art_storage.check_fit_by_object_id_and_dimensions(art_object_id, dimensions_user_ordered)
