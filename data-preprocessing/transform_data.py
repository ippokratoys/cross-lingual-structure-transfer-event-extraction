"""
Transform the RAMS data to a json that will be used
in order to apply event extraction. The target JSON
file will have the following format
[{
  sentence: "I will travel to Greece next week."
  event: TRANSFER
}]
"""
import argparse
import json
from pathlib import Path

from corpy.udpipe import Model

m = Model("./data/english-ewt-ud-2.5-191206.udpipe")


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
    If a event exists it returns the event as a string else NONE
    """
    for event in events:
        event_start = event[0]
        event_end = event[1]
        event = event[2][0][0]
        if sentence_start_index <= event_start <= sentence_end_index:
            return event
        if sentence_start_index <= event_end <= sentence_end_index:
            return event

    return None


def convert_line_to_target(line):
    """
    Given a line of .jsonline parse the line and convert it to a list of sentences
    with their event
    :param line: a line from RAMS dataset
    :return: a list of sentence with events
    """
    data = json.loads(line)
    events = data['evt_triggers']
    sentences = data['sentences']
    sentence_start_index = 0
    sentences_converted = []
    for sentence_tokes in sentences:
        sentence_end_index = sentence_start_index + len(sentence_tokes)

        entry = dict()
        entry['sentence'] = " ".join(sentence_tokes)
        entry['tokens'] = map_tokens(entry['sentence'])

        sentence_event = get_event(events, sentence_start_index, sentence_end_index)
        if sentence_event is None:
            entry['event'] = 'NONE'
        else:
            entry['event'] = sentence_event

        sentence_start_index = sentence_end_index
        sentences_converted.append(entry)

    return sentences_converted


def transform_from_file_to_file(source_file_path, target_file_path):
    with open(source_file_path, "r") as read_file:
        sentences = []
        for line in read_file:
            sentences.extend(convert_line_to_target(line))

        path = Path(target_file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(target_file_path, "w") as write_file:
            json.dump(sentences, write_file, separators=(',', ':'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', default="data/rams/dev.jsonlines")
    parser.add_argument('--target', default="data/parsed/dev.json")
    args = parser.parse_args()
    print("Converting {" + args.source + "} to {" + args.target + "}")
    transform_from_file_to_file(args.source, args.target)
