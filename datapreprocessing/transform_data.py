"""
Transform the RAMS data to a json that will be used
in order to apply event extraction. The target JSON
file will have the following format
[{
  sentence: "I will travel to Greece next week.",
  tokens: [{
    text: "I"
    part_of_speech: "VERB"
    id: 3,
    dependency_relation: "SUBJ"
    head: 1,
    word_embeddings: [...]
  }]
  event: TRANSFER
}]
"""
import argparse
import json
import random
import uuid
from pathlib import Path

import stanza
from corpy.udpipe import Model
from tqdm import tqdm

LANG_SPECIFIC_OPTIONS = {
    "en": {
        "model_ud_pipe": "./data/english-ewt-ud-2.5-191206.udpipe",
        "fasttext_lang": "en",
        "fasttext_model": "./dataset/fasttext/wiki.en.align.vec",
        "stanza_download": "en",
        "stanza_pipeline": "en",
    },
    # not used right now
    "fr": {
        "model_ud_pipe": "./data/french-gsd-ud-2.5-191206.udpipe",
        "fasttext_lang": "fr",
        "fasttext_model": "cc.fr.300.bin",
        "stanza_download": "fr",
        "stanza_pipeline": "fr"
    },
    "de": {
        "model_ud_pipe": "./data/german-gsd-ud-2.5-191206.udpipe",
        "fasttext_lang": "de",
        "fasttext_model": "./dataset/fasttext/wiki.de.align.vec",
        "stanza_download": "de",
        "stanza_pipeline": "de"
    }
}


def init_models(lang="en"):
    global m
    global ft
    global stanza_nlp

    if lang not in LANG_SPECIFIC_OPTIONS.keys():
        print("Can't handle lang", lang)
        exit(42)
    options = LANG_SPECIFIC_OPTIONS[lang]

    # see {http://lindat.mff.cuni.cz/services/udpipe/} for different language models
    # see {https://universaldependencies.org/format.html}
    m = Model(options["model_ud_pipe"])

    stanza.download(options["stanza_download"])
    stanza_nlp = stanza.Pipeline(options["stanza_pipeline"], processors='tokenize,ner')


def map_word_to_token(word):
    """
    Given a sentence return a list of tokens with the required data

    :param sentence: a sentence
    :return: a list of sentence with events
    """
    token = {}
    token['text'] = word.form
    token['part_of_speech'] = word.upostag
    token['id'] = word.id
    token['dependency_relation'] = word.deprel
    token['head'] = word.head
    # token['word_embeddings'] = ft.get_word_vector(word.form).tolist()
    return token


def map_tokens(sentence):
    """
    :param sentence: a sentence as string
    :return: a list of tokens with the required data
    """
    parsed = list(m.process(sentence))
    return list(map(map_word_to_token, parsed[0].words[1:]))


def get_event(events, sentence_start_index, sentence_end_index):
    """
    Returns whether a sentence given its start/end index contains an event.
    If a event exists it returns the event as a string and it's relative to sentence start/end index else NONE
    """
    for event in events:
        event_start = event[0]
        event_end = event[1]
        event_label = event[2][0][0]
        if sentence_start_index <= event_start <= sentence_end_index:
            return event_label, (event_start - sentence_start_index), (event_end - sentence_start_index)

    return None, None, None


def get_argument(arguments, sentence_start_index, sentence_end_index):
    """
    Returns whether a sentence given its start/end index contains an argument.
    If an argument exists it returns it's relative to sentence start/end index else NONE
    """
    for argument in arguments:
        argument_start = argument[1][0]
        argument_end = argument[1][1]
        if sentence_start_index <= argument_start <= sentence_end_index:
            return (argument_start - sentence_start_index), (argument_end - sentence_start_index)

    return None, None


def convert_line_to_target(line):
    """
    Given a line of .jsonline parse the line and convert it to a list of sentences
    with their event
    :param line: a line from RAMS dataset
    :return: a list of sentence with events
    """
    data = json.loads(line)
    events = data['evt_triggers']
    gold_evt_links = data['gold_evt_links']
    sentences = data['sentences']
    sentence_start_index = 0
    sentences_converted = []
    for sentence_tokens in sentences:
        sentence_end_index = sentence_start_index + len(sentence_tokens) - 1

        entry = dict()
        entry['id'] = str(uuid.uuid4())
        entry['sentence'] = " ".join(sentence_tokens)
        tokens_with_data = map_tokens(entry['sentence'])
        entry['token_ud'] = list(map(lambda x: x['text'], tokens_with_data))
        # todo check if we can skip tokenization
        parsed = stanza_nlp.process(entry['sentence'])

        entry['token'] = []
        entry['stanford_ner'] = []
        entry['stanford_pos'] = list(map(lambda x: x['part_of_speech'], tokens_with_data))
        entry['stanford_head'] = list(map(lambda x: x['head'], tokens_with_data))
        entry['stanford_deprel'] = list(map(lambda x: x['dependency_relation'], tokens_with_data))
        for index, token in enumerate(parsed.sentences[0].tokens):
            entry['token'].append(token.text)
            entry['stanford_ner'].append(token.ner)

        if len(entry['token_ud']) != len(entry['token']) or len(entry['token_ud']) != len(sentence_tokens):
            # global skipped_sentences
            # skipped_sentences += 1
            sentence_start_index = sentence_end_index + 1
            continue

        sentence_event, sentence_event_start, sentence_event_stop = get_event(events, sentence_start_index,
                                                                              sentence_end_index)
        if sentence_event is None:
            entry['relation'] = 'no_relation'

            subj_start = random.randint(0, len(entry['token']) - 1)

            entry['subj_start'] = subj_start
            entry['subj_end'] = subj_start
            entry['subj_type'] = entry["stanford_pos"][subj_start]

            obj_start = random.randint(0, len(entry['token']) - 1)
            for i in range(100):
                if subj_start != obj_start:
                    break
                obj_start = random.randint(0, len(entry['token']) - 1)

            entry['obj_start'] = obj_start
            entry['obj_end'] = obj_start
            entry['obj_type'] = entry["stanford_ner"][obj_start]
        else:
            entry['relation'] = sentence_event
            entry['subj_start'] = sentence_event_start
            entry['subj_end'] = sentence_event_stop
            entry['subj_type'] = entry['stanford_pos'][sentence_event_start]

            sentence_argument_start, sentence_argument_stop = get_argument(gold_evt_links, sentence_start_index,
                                                                           sentence_end_index)

            if sentence_argument_start is None:
                obj_start = random.randint(0, len(entry['token']) - 1)

                entry['obj_start'] = obj_start
                entry['obj_end'] = obj_start
                entry['obj_type'] = entry["stanford_ner"][obj_start]
            else:
                entry['obj_start'] = sentence_argument_start
                entry['obj_end'] = sentence_argument_stop
                entry['obj_type'] = entry['stanford_ner'][sentence_event_start]

        sentence_start_index = sentence_end_index + 1
        sentences_converted.append(entry)
    return sentences_converted


def transform_from_file_to_file(source_file_path, target_file_path, target_file_for_translation_path):
    num_lines = sum(1 for _ in open(source_file_path, 'r'))
    with open(source_file_path, "r") as read_file:
        sentences = []
        sentences_to_translate = []
        for line in tqdm(read_file, total=num_lines):
            converted_sentences = convert_line_to_target(line)
            sentences.extend(converted_sentences)
            sentences_to_translate.extend(converted_sentence['sentence'] for converted_sentence in converted_sentences)

        path = Path(target_file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        print("Writing to target file")
        with open(target_file_path, "w") as write_file:
            json.dump(sentences, write_file, separators=(',', ':'))

        path_for_translation = Path(target_file_for_translation_path)
        path_for_translation.parent.mkdir(parents=True, exist_ok=True)
        print("Writing to target translation file")
        with open(target_file_for_translation_path, "w") as write__translation_file:
            json.dump(sentences_to_translate, write__translation_file, separators=(',', ':'))


def convert_to_sentences_of_tokens(text):
    parsed = list(m.process(text))
    sentences = []
    for sentence_parsed in parsed:
        sentence = []
        for word in sentence_parsed.words[1:]:
            sentence.append(word.form)
        sentences.append(sentence)
    return sentences


def parse_single(text, target_file_path, lang):
    init_models(lang)
    sentences_of_tokens = convert_to_sentences_of_tokens(text)
    line = """
    {{
      "sentences": {},
      "evt_triggers": [],
      "gold_evt_links": [] 
    }}
    """.format(json.dumps(sentences_of_tokens))
    sentences = convert_line_to_target(line)
    sentences_all_possible = []
    for sentence in sentences:
        for i in range(len(sentence['token'])):
            for j in range(len(sentence['token'])):
                if i == j:
                    continue
                new_sentence = sentence.copy()
                new_sentence['obj_start'] = i
                new_sentence['obj_end'] = i
                new_sentence['obj_type'] = sentence["stanford_ner"][i]

                new_sentence['subj_start'] = j
                new_sentence['subj_end'] = j
                new_sentence['subj_type'] = sentence['stanford_pos'][j]

                sentences_all_possible.append(new_sentence)
    path = Path(target_file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    print("Writing to file")
    with open(target_file_path, "w") as write_file:
        json.dump(sentences_all_possible, write_file, separators=(',', ':'))


def parse_single_return(text):
    sentences_of_tokens = convert_to_sentences_of_tokens(text)
    line = """
    {{
      "sentences": {},
      "evt_triggers": [] ,
      "gold_evt_links": []
    }}
    """.format(json.dumps(sentences_of_tokens))
    sentences = convert_line_to_target(line)

    return sentences


if __name__ == '__main__':
    # global skipped_sentences
    # skipped_sentences = 0
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', default="data/rams/dev.jsonlines")
    parser.add_argument('--target', default="data/parsed/dev.json")
    parser.add_argument('--target_translation', default="data/parsed/dev_translation.json")
    parser.add_argument('--lang', default="en")
    args = parser.parse_args()
    print("Converting {" + args.source + "} to {" + args.target + "}")
    print("Loading models...")
    init_models(args.lang)
    print("Done loading")
    transform_from_file_to_file(args.source, args.target, args.target_translation)
    # print("Skipped ", skipped_sentences, "sentences due to tokenizer ner and pos missalign")
