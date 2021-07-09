import argparse
import json
import random


def mask_objects(source_file_path):
    print("Loading file...")
    with open(source_file_path) as infile:
        target_lang_sentences = json.load(infile)

    updated = []
    print("Converting classes...")
    for sentence in target_lang_sentences:

        updated_sentence = sentence

        if sentence['relation'] != 'no_relation':
            updated.append(updated_sentence)
            continue

        obj_start = random.randint(0, len(sentence['token']) - 1)

        updated_sentence['obj_start'] = obj_start
        updated_sentence['obj_end'] = obj_start
        updated_sentence['obj_type'] = sentence["stanford_ner"][obj_start]

        subj_start = random.randint(0, len(sentence['token']) - 1)
        for i in range(100):
            if subj_start != obj_start:
                break
            subj_start = random.randint(0, len(sentence['token']) - 1)

        updated_sentence['subj_start'] = subj_start
        updated_sentence['subj_end'] = subj_start
        updated_sentence['subj_type'] = sentence["stanford_pos"][subj_start]
        updated.append(updated_sentence)

    print("Updating file...")
    with open(source_file_path, "w") as write_file:
        json.dump(updated, write_file, separators=(',', ':'))


if __name__ == '__main__':
    global skipped_sentences

    parser = argparse.ArgumentParser()
    parser.add_argument('--source', default="data/parsed/dev.json")
    args = parser.parse_args()

    mask_objects(args.source)
