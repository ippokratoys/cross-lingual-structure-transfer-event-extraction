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
from pathlib import Path

from tqdm import tqdm


def convert_to_simple_event(original_event):
    if "." in original_event:
        return original_event.split(".")[0]
    return original_event


def trim_events(source_file_path):
    print("Loading file...")
    with open(source_file_path) as infile:
        target_lang_sentences = json.load(infile)

    original_events_set = set()
    updated_events_set = set()
    updated = []
    print("Converting classes...")
    for sentence in target_lang_sentences:
        original_event = sentence['relation']
        updated_event = convert_to_simple_event(original_event)

        updated_sentence = sentence
        updated_sentence['relation'] = updated_event
        updated_sentence['event'] = original_event

        original_events_set.add(original_event)
        updated_events_set.add(updated_event)
        updated.append(updated_sentence)

    print("Updating file...")
    with open(source_file_path, "w") as write_file:
        json.dump(updated, write_file, separators=(',', ':'))

    print("--- Original ---\n", original_events_set)
    print("--- Updated  ---\n", updated_events_set)
    print("Events reduced from size", len(original_events_set), "to", len(updated_events_set))
    print("Don't forget to update constant.py. You can use helper.py.")



if __name__ == '__main__':
    global skipped_sentences

    parser = argparse.ArgumentParser()
    parser.add_argument('--source', default="data/parsed/dev.json")
    args = parser.parse_args()

    trim_events(args.source)
