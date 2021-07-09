import argparse
import json


def convert_to_simple_event(original_event):
    if "." in original_event:
        return original_event.split(".")[0]
    return original_event


def mask_objects(source_file_path):
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
        updated_sentence['obj_start'] = 0
        updated_sentence['obj_end'] = 0
        updated_sentence['obj_type'] = sentence["stanford_ner"][0]

        last_token = len(updated_sentence['tokens']) - 1
        updated_sentence['subj_start'] = last_token
        updated_sentence['subj_end'] = last_token
        updated_sentence['subj_type'] = sentence["stanford_pos"][last_token]

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

    mask_objects(args.source)
