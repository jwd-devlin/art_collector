# art_collector

## Introduction:

Data about the art sourced via the Met Museum Github (https://github.com/metmuseum/openaccess/). * Note need to download
the data and place in "src/resources/MetObjects.txt".

- Project Business Logic:
  Users would like to be able to determine if a piece of art would fit within their current living space. They would be
  able to provide a set of 3-D measurements (length, width, height) and a known objectID corresponding to their desired
  piece.


- Data Cleaning Assumptions/Observations.

  - Gathering data:
    - Preference given to the maximum number for a give spatial direction ( length, width, height)
  - Measurement Directions.
    - Measurement flags have been noted with letters ( H, L, Diam, Th, W)
    - Or without just maintaining a separation with "x", ";" or ","
    - Diameter measurements equate to Length x Width measurements.
  - Measurement Units.
    - Metric values and Imperial values appear in brackets () separately.
    - Metric units may also appear alone.
    - Measurements without units will be considered lost.
  - Incorrect values (Aim for the majority of data that follows consistent rules).
    - Values with fractions like 3 1/2 for cm units will be ignored.
    - Errors with "2.." will also be ignored.
    - Somethings just cause too much pain: "Storage: 40.5 cm, 60 1/2 in. (15 15/16 in., 153.7 cm)"

  - Cleaning Logic:
    1) Check the data for cm. 2a) find any mention of the measurement directions ( length, width, height) and their
       order of occurrence. 2b) extract the numbers associated with cm units.
    3) Map the directions with the cm associated numbers.

## To Run:

- Start-Up:
  - Use the docker-compose.yml to start up the containers ( Postgres, Jupyter notebook).
    - Included is the setup of the database with the migration container.

    ```docker compose up --build```

- Setup DataPipeline Run:
  - dimension extraction logic can be found in "src/main/data_pipeline/data_transform/dimension_extractor.py"
  - Run the ETL Pipeline using the /src/Project_ETL.ipynb.

- Application Run:
  - Run the /src/Find_me_art.ipynb
  - See notebook for examples of finding art for your home.
  - Assumption that the user will always provide a dictionary of volume information, so three measurements one for the
    (length, width, height).
    - "Wild assumption" that the users pick the same orientation as the measurements were intended.

## Additional Notes:

- Pipeline Improvements:
  - *Ways to improve.
  - Move initial raw data to S3 or other cloud storage.
  - Move this to data pipeline workflow management helper: Airflow.
  - parallelise the ETL.
  - Move cleaning to spark for speed up.
  - clean up: move sql to a separate file.

- Cleaned data Storage Format: Postgres
  - Due to the nature of the measurement data, having an innate structure and being relatively "simple" homogeneous. It
    made sense to have a storage solution that would also suit a relational store. Additional the for the current
    application the query for retrieving the data was a key-value query.
  - I kept the business logic for the "does_it_fit" from being intertwined with the storage solution. To allow for
    potential switching of storage options, and "aid" in speed of return.
  - Flexible solution for more/new logic.
  - Free.

