"""
In order to run align.py you need to first download the desired languages + english vectors from
https://fasttext.cc/docs/en/aligned-vectors.html
After that, LANG_SPECIFIC_OPTIONS should be updated with the correct path.
Run this script in order to load the files in a faster format.

Then you can run the align_lang with the desired params
"""
from gensim.models import KeyedVectors

from datapreprocessing.transform_data import LANG_SPECIFIC_OPTIONS

wv_from_text = KeyedVectors.load_word2vec_format(LANG_SPECIFIC_OPTIONS["de"]["fasttext_model"],
                                                 binary=False)  # C text format

wv_from_text.save(LANG_SPECIFIC_OPTIONS["de"]["fasttext_model"][:-3] + "out")

wv_from_text = KeyedVectors.load_word2vec_format(LANG_SPECIFIC_OPTIONS["en"]["fasttext_model"],
                                                 binary=False)  # C text format

wv_from_text.save(LANG_SPECIFIC_OPTIONS["en"]["fasttext_model"][:-3] + "out")
