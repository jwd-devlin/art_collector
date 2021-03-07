-- base-line
--- Art Dimensions
DROP TABLE IF EXISTS art_dimensions;
CREATE TABLE IF NOT EXISTS art_dimensions
(
    object_id
    INT,
    dimensions
    TEXT,
    art_length
    FLOAT,
    art_width
    FLOAT,
    art_height
    FLOAT,
    PRIMARY
    KEY
(
    object_id
)
    );
CREATE
INDEX IF NOT EXISTS ix_object_id ON art_dimensions (object_id);

