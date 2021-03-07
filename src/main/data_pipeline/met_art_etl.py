from src.main.data_pipeline.data_extraction.met_art_extractor import MetArtExtractor
from src.main.data_pipeline.data_transform.met_art_transform import MetArtTransform
from src.main.data_pipeline.storage.art_storage import ArtStorage
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug_etl.log"),
        logging.StreamHandler()
    ]
)


class MetaArtETL:
    CHUNK_SIZE = 10000
    EXTRACTED_COLUMNS = ["Object ID", "Dimensions"]
    TRANSFORMED_DATA_COLUMNS = ["Length", "Width", "Height"]
    TABLE_NAME = "art_dimensions"

    def __init__(self, extractor: MetArtExtractor, transformer: MetArtTransform, storage: ArtStorage):
        self.extractor = extractor
        self.transformer = transformer
        self.storage = storage

    def execute(self, source_file_location: str, tester: bool = False) -> None:

        data_frames = self.extractor.read_csv_batch(source_file_location, interest_columns=self.EXTRACTED_COLUMNS,
                                                    chunk_size=self.CHUNK_SIZE)

        for index, data_frame in enumerate(data_frames):
            logging.info("Processing %s data frame", index + 1)

            cleaned_art_data = self.transformer.execute(data_frame)

            self.storage.insert_dataframe(cleaned_art_data.columns.tolist(), cleaned_art_data,
                                          self.TABLE_NAME)
            if tester:
                break


if __name__ == '__main__':
    location = "resources/MetObjects.txt"
    MetaArtETL(MetArtExtractor(), MetArtTransform(), ArtStorage(user="arty", password="pwd",
                                                                host="postgres")).execute(location, False)
