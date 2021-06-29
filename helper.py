"""
Helper for extracting unique values to use as keys in constant.py
"""
import argparse
import json


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


def convert_line_to_events(line):
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
    all_events = set()
    for sentence_tokes in sentences:
        sentence_end_index = sentence_start_index + len(sentence_tokes)

        entry = dict()
        sentence_event = get_event(events, sentence_start_index, sentence_end_index)
        if sentence_event is None:
            entry['relation'] = 'no_relation'
        else:
            all_events.add(sentence_event)
            entry['relation'] = sentence_event

        sentence_start_index = sentence_end_index
        sentences_converted.append(entry)

    return all_events


def get_subj_ner_to_id(entry):
    """SUBJ_NER_TO_ID"""
    val = entry['subj_type']
    if val not in ['<PAD>', '<UNK>', 'no_relation']:
        return {val}
    else:
        return {}


def get_obj_ner_to_id(entry):
    """OBJ_NER_TO_ID"""
    val = entry['obj_type']
    if val not in ['<PAD>', '<UNK>', 'no_relation']:
        return {val}
    else:
        return {}


def get_ner_to_id(entry):
    """NER_TO_ID"""
    list_val = entry['stanford_ner']
    ret = set()
    for val in list_val:
        if val not in ['<PAD>', '<UNK>', 'no_relation']:
            ret.add(val)
    return ret


def get_pos_to_id(entry):
    """POS_TO_ID"""
    list_val = entry['stanford_pos']
    ret = set()
    for val in list_val:
        if val not in ['<PAD>', '<UNK>', 'no_relation']:
            ret.add(val)
    return ret


def get_deprel_to_id(entry):
    """DEPREL_TO_ID"""
    list_val = entry['stanford_deprel']
    ret = set()
    for val in list_val:
        if val not in ['<PAD>', '<UNK>', 'no_relation']:
            ret.add(val)
    return ret


def get_label_to_id(entry):
    """LABEL_TO_ID"""
    val = entry['relation']
    if val not in ['<PAD>', '<UNK>', 'no_relation']:
        return {val}
    else:
        return {}


def print_distict_values(filename):
    extractors = [
        get_subj_ner_to_id,
        get_obj_ner_to_id,
        get_ner_to_id,
        get_pos_to_id,
        get_deprel_to_id,
        get_label_to_id
    ]
    min_id = [
        2,  # get_subj_ner_to_id,
        2,  # get_obj_ner_to_id,
        2,  # get_ner_to_id,
        2,  # get_pos_to_id,
        2,  # get_deprel_to_id,
        1  # get_label_to_id
    ]
    values = [set() for _ in extractors]
    with open(filename) as infile:
        data = json.load(infile)
    for entry in data:
        for index, extractor in enumerate(extractors):
            values[index] = values[index].union(extractor(entry))

    for index, extractor in enumerate(extractors):
        print("------------", extractor.__doc__, "-------------")
        dict = {}
        for i, val in enumerate(values[index]):
            dict[val] = i + min_id[index]
        print(dict)
        print("--------------------------")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # parser.add_argument('--source', default="data/rams/train.jsonlines")
    parser.add_argument('--source', default="data/parsed/dev.json")
    args = parser.parse_args()
    print("Printing distinct values {" + args.source + "}")
    print_distict_values(args.source)
