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

# Train model

## English train over RAMS dataset

1. Pre-process rams

- Dev

`python3 datapreprocessing/transform_data.py --source data/rams/dev.jsonlines --target data/parsed/dev.json --target_translation data/parsed/dev_translation.json`

- Test

`python3 datapreprocessing/transform_data.py --source data/rams/test.jsonlines --target data/parsed/test.json --target_translation data/parsed/test_translation.json`

- Train

`python3 datapreprocessing/transform_data.py --source data/rams/train.jsonlines --target data/parsed/train.json --target_translation data/parsed/train_translation.json`

_The `data/parsed/train_translation.json` can be used to translate and align the dataset when a different language is
used._

3. As mentioned in gcn github

`python3 prepare_vocab.py data/parsed dataset/vocab`

4. Train the model

`python3 train.py --id 0 --seed 0 --lr 0.3 --no-rnn --num_epoch 100 --pooling max --mlp_layers 2 --pooling_l2 0.003`

5. Eval

`python3 eval.py saved_models/00 --dataset dev --data_dir data/parsed`

5. Inference

`python3 inference.py saved_models/00 --dataset dev --data_dir data/parsed`

6. Evaluate in a different language (requires pre-processing)
   Assuming that the target language already exists:
    - Prepare vocab for target language (make sure to replace .vec with your paths)
      `python3 prepare_vocab.py data/parse_de dataset/vocab_de --glove_dir /media/thanasis/Elements/university/nlp --wv_file wiki.de.align.vec`
    - Run
      `python3 eval.py saved_models/00 --dataset test --data_dir data/parse_de --vocab_file dataset/vocab_de/vocab.pkl`
