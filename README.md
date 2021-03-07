# art_collector

## Introduction:

Data about the art sourced via the Met Museum Github (https://github.com/metmuseum/openaccess/).

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
  - Measurement Units.
    - Metric values and Imperial values appear in brackets () separately.
    - Metric units may also appear alone.
    - Measurements without units will be considered lost.
  - Incorrect values.
    - Values with fractions like 3 1/2 for cm units will be ignored.
    - Errors with 2.. will also be ignored.
    - Somethings just cause too much pain: "Storage: 40.5 cm, 60 1/2 in. (15 15/16 in., 153.7 cm)"

## To Run:
