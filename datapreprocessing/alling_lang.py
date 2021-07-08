"""
Given a list of german sentences and a file containing complete data in English.
Create an identical json (with udpipe, event, trigger etc) for the german language)
"""
import argparse
import json

import numpy
from gensim.models import KeyedVectors

from datapreprocessing.transform_data import init_models, LANG_SPECIFIC_OPTIONS
from datapreprocessing.transform_data import parse_single_return


def init_vectors(lang="en"):
    global key_vectors_en
    global key_vectors_lang

    options = LANG_SPECIFIC_OPTIONS[lang]

    key_vectors_en = KeyedVectors.load(LANG_SPECIFIC_OPTIONS["en"]["fasttext_model"][:-3] + "out")
    key_vectors_lang = KeyedVectors.load(options["fasttext_model"][:-3] + "out")


def index_of_type(target_type, target_parsed, key):
    result = set()
    for index, val in enumerate(target_parsed[key]):
        if val == target_type:
            result.add(index)
    return result


def get_vector_en(word):
    global key_vectors_en
    try:
        return key_vectors_en[word.lower()]
    except Exception as e:
        return [0] * 300


def get_vector_lang(word):
    global key_vectors_lang
    try:
        return key_vectors_lang[word.lower()]
    except Exception as e:
        return [0] * 300


def find_index_of_word_vector(index, source_parsed, target_parsed):
    source_vector = get_vector_en(source_parsed['token'][index])
    distances = []
    for token in target_parsed['token']:
        target_vectors = get_vector_lang(token)
        distances.append(numpy.linalg.norm(source_vector - target_vectors))
    index_min = numpy.argmin(distances)
    return int(index_min)


# def find_index_of_word(index, source_parsed, target_parsed):
#     """
#     Deprecated. Use find_index_of_word_vector instead.
#     Might miss more than 30% the sentences
#     :param index:
#     :param source_parsed:
#     :param target_parsed:
#     :return:
#     """
#
#     deprel_indexs = index_of_type(source_parsed['stanford_deprel'][index], target_parsed, 'stanford_deprel')
#     if len(deprel_indexs) == 1:
#         print('stanford_deprel')
#         return next(iter(deprel_indexs))
#
#     pos_indexes = index_of_type(source_parsed['stanford_pos'][index], target_parsed, 'stanford_pos')
#     if len(pos_indexes) == 1:
#         print('stanford_pos')
#         return next(iter(pos_indexes))
#
#     ner_indexes = index_of_type(source_parsed['stanford_ner'][index], target_parsed, 'stanford_ner')
#     if len(ner_indexes) == 1:
#         print('stanford_ner')
#         return next(iter(ner_indexes))
#
#     # todo: should joint all by 1, in order to make sure that if
#     common = deprel_indexs.intersection(pos_indexes).intersection(ner_indexes)
#     if len(common) == 1:
#         print("common")
#         return next(iter(common))
#
#     for possible_index in common.copy():
#         parrent_source_index = source_parsed['stanford_head'][index]
#         parrent_possible_index = target_parsed['stanford_head'][possible_index]
#         if source_parsed['stanford_deprel'][parrent_source_index] != source_parsed['stanford_deprel'][
#             parrent_possible_index]:
#             common.remove(possible_index)
#
#     if len(common) == 1:
#         print('head_indexes')
#         return next(iter(common))
#
#     print("NOTHING MATCHED...", deprel_indexs, pos_indexes, ner_indexes, sep="\n")
#     return 0


def align_languages(source_lang_filename, target_lang_sentences_filename, out_lang_filename):
    global skipped_sentences
    with open(source_lang_filename) as infile:
        source_lang_data = json.load(infile)

    with open(target_lang_sentences_filename) as infile:
        target_lang_sentences = json.load(infile)

    target_list = []
    for i, _ in enumerate(source_lang_data):
        source_lang = source_lang_data[i]
        target_lang_sentence = target_lang_sentences[i]
        target_parsed = parse_single_return(target_lang_sentence)

        if len(target_parsed) > 1:
            skipped_sentences += 1
            print("Maps to more than one sentence. SKIPPING sentence...")
            continue

        target_parsed = target_parsed[0]

        target_parsed['id'] = source_lang['id']
        target_parsed['relation'] = source_lang['relation']
        if source_lang['subj_start'] != -1:
            index = find_index_of_word_vector(source_lang['subj_start'], source_lang, target_parsed)
            target_parsed['subj_start'] = index
            target_parsed['subj_end'] = index
            target_parsed['subj_type'] = source_lang['subj_type']

        if source_lang['obj_start'] != -1:
            index = find_index_of_word_vector(source_lang['obj_start'], source_lang, target_parsed)
            target_parsed['obj_start'] = index
            target_parsed['obj_end'] = index
            target_parsed['obj_type'] = source_lang['obj_type']

        target_list.append(target_parsed)

    with open(out_lang_filename, "w") as write_file:
        json.dump(target_list, write_file, separators=(',', ':'))


if __name__ == '__main__':
    global skipped_sentences
    skipped_sentences = 0
    parser = argparse.ArgumentParser()
    parser.add_argument('--source_english', default="data/parsed/dev.json")
    parser.add_argument('--source_target', default="data/parsed/dev_translation_de.json")
    parser.add_argument('--out_target', default="data/parsed/dev_de.json")
    parser.add_argument('--lang', default="de")
    args = parser.parse_args()
    print("Converting ", args.source_english, " with translated sentences ", args.source_target, "(lang=", args.lang,
          ")")
    print("Will write output to", args.out_target)
    print("Loading models...")
    init_models(args.lang)
    print("Loading vectors...")
    init_vectors(args.lang)
    print("Done loading")
    align_languages(args.source_english, args.source_target, args.out_target)
    print("Skipped ", skipped_sentences, "sentences due to tokenizer ner and pos missalign")
