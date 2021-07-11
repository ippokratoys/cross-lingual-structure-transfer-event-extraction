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


def align_indices(de1, de2):
    key = len(de1.keys())
    for key2 in de2.keys():
        de1[str(key)] = de2[key2]
        key += 1
    return de1


def align_files(source_file_path, dest_file_path):
    print("Loading file...")
    with open(source_file_path, encoding='utf8') as infile:
        sentences1 = json.load(infile)

    with open(dest_file_path, encoding='utf8') as outfile:
        sentences2 = json.load(outfile)

    result = align_indices(sentences2, sentences1)

    print("Updating file...")
    with open(dest_file_path, "w") as write_file:
        json.dump(result, write_file, separators=(',', ':'))



if __name__ == '__main__':
    global skipped_sentences

    parser = argparse.ArgumentParser()
    parser.add_argument('--source', default="data/parsed/de1.json")
    parser.add_argument('--dest', default="data/parsed/de.json")
    args = parser.parse_args()

    align_files(args.source, args.dest)
