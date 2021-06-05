# cross-lingual-structure-transfer-event-extraction
Implementation of Cross-lingual Structure Transfer for Relation and Event Extraction

## Data pre-processing

In order to pre-process the data use the script given in `data-preprocessing/`.

### Convert Rams data
In order to convert RAMS data use transform_data.py. It takes two arguments `--source` 
for defining the source file (see `data/rams`) and `--target` to define the output file

e.g `python data-preprocessing/transform_data.py --source data/rams/dev.jsonlines --target data/parsed/dev.json`