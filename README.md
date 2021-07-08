# cross-lingual-structure-transfer-event-extraction

Implementation of Cross-lingual Structure Transfer for Relation and Event Extraction

## Data pre-processing

In order to pre-process the data use the script given in `data-preprocessing/`.

### Convert Rams data

In order to convert RAMS data use transform_data.py. It takes two arguments `--source`
for defining the source file (see `data/rams`) and `--target` to define the output file

e.g `python data-preprocessing/transform_data.py --source data/rams/dev.jsonlines --target data/parsed/dev.json`

### Different language preprocessing

1. Run`transform_data.py` for the English dataset
2. Manually translate the `dev_translation.json`. Make sure not maintain the same order.
3. Download https://fasttext.cc/docs/en/aligned-vectors.html
4. Update `LANG_SPECIFIC_OPTIONS` with the correct path
5. Run `convert_vec_to_bin.py`
6. Run `allign_lang.py`

This will produce a `dev_translation_de.json` which contains all the data from `dev.json` by using
`dev_translation_de.json`.

# Current commands to test the model

1. Pre-process rams

`python3 datapreprocessing/transform_data.py`

2. Use dev.json both as test and train set

`cp data/parsed/dev.json data/parsed/test.json; cp data/parsed/dev.json data/parsed/train.json`

3. As mentioned in gcn github

`python3 prepare_vocab.py data/parsed dataset/vocab`

4. Train the model

`python3 train.py --id 0 --seed 0 --lr 0.3 --no-rnn --num_epoch 100 --pooling max --mlp_layers 2 --pooling_l2 0.003`
With prunning as gcn readme (not working)
(`python3 train.py --id 0 --seed 0 --prune_k 1 --lr 0.3 --no-rnn --num_epoch 100 --pooling max --mlp_layers 2 --pooling_l2 0.003`)

5. Inference

`python3 inference.py saved_models/00 --dataset single --data_dir data/parsed`

