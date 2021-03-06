import pandas as pd


class MetArtExtractor:

    @staticmethod
    def read_csv_batch(location: str, interest_columns: list, chunk_size: int) -> pd.io.parsers.TextFileReader:
        return pd.read_csv(location, usecols=interest_columns, chunksize=chunk_size)
