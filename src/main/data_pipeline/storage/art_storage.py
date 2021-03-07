import pandas as pd
import psycopg2


class ArtStorage:
    def __init__(self, user="", password="", host="postgres", port=5432, database="art") -> None:
        super().__init__()
        self._database = database
        self._port = port
        self._host = host
        self._password = password
        self._user = user
        self._writing_connection = None
        self._reading_connection = None

    def get_conn(self):
        return psycopg2.connect(user=self._user,
                                password=self._password,
                                host=self._host,
                                port=self._port,
                                database=self._database)

    def __prepare_writing(self):
        if self._writing_connection is None:
            self._writing_connection = self.get_conn()
        return self._writing_connection

    def __prepare_reading(self):
        if self._reading_connection is None:
            self._reading_connection = self.get_conn()
        return self._reading_connection

    def commit_write(self) -> None:
        connection = self.__prepare_writing()
        connection.commit()

    def insert_dataframe(self, query_columns: list, data: pd.DataFrame, table_name: str) -> None:
        query = self.__insert_query_builder(query_columns, table_name)
        for index, row in data.iterrows():
            self.__write_row(query, row[query_columns])
        self.commit_write()

    def __write_row(self, query, values: list):
        connection = self.__prepare_writing()
        with connection.cursor() as cursor:
            cursor.execute(query, tuple(values))

    def __insert_query_builder(self, fields: list, table_name: str) -> str:
        fill_in_field_spots = ", ".join(["%s" for item in fields])
        fill_in_field_names = ", ".join(fields)
        return f"""INSERT INTO {table_name} ( {fill_in_field_names} ) VALUES ( {fill_in_field_spots} ) 
                   ON CONFLICT DO NOTHING"""

    def read_dimensions_by_object_id(self, object_id: int, table_name: str = "art_dimensions"):
        read_query = f"""SELECT * FROM {table_name} WHERE object_id = %s;"""
        connection = self.__prepare_reading()
        return pd.read_sql_query(read_query, params=[
            object_id
        ], con=connection)
