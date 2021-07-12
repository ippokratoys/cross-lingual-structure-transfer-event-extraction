import json
import re


def pre_process(filename, write_filename):
    with open(filename, "r") as read_file:
        data = json.load(read_file)
        sentences = []
        for entry in data:
            for sentence_index, sentence_unparsed in enumerate(entry['sentences']):
                start_index = sentence_unparsed['start']
                end_index = sentence_unparsed['end']
                sentence = {}
                sentence["id"] = entry["id"]

                sentence["sentence"] = sentence_unparsed['text']

                sentence["token"] = entry["words"][start_index:end_index]
                sentence["stanford_ner"] = entry["ner"][start_index:end_index]
                # needs mapping
                sentence["stanford_pos"] = entry['pos-tags'][start_index:end_index]
                sentence["stanford_head"] = list(
                    map(lambda x: int(re.search("dep=\d", x)[0].split("=")[1]),
                        entry['dependency-parsing'][sentence_index]))
                sentence["stanford_deprel"] = list(
                    map(lambda x: x.split("/")[0], entry['dependency-parsing'][sentence_index]))
                sentence["relation"] = "no_relation"

                sentence["subj_start"] = 0
                sentence["subj_end"] = 0
                sentence["subj_type"] = '<UNK>'

                sentence["obj_start"] = 1
                sentence["obj_end"] = 1
                sentence["obj_type"] = '<UNK>'

                sentences.append(sentence)

        sentences_all_possible = []
        for sentence in sentences:
            for i in range(len(sentence['token'])):
                for j in range(len(sentence['token'])):
                    if i == j:
                        continue
                    sentence_copy = sentence.copy()

                    sentence_copy["subj_start"] = i
                    sentence_copy["subj_end"] = i
                    sentence_copy["subj_type"] = sentence['stanford_pos'][i]

                    sentence_copy["obj_start"] = j
                    sentence_copy["obj_end"] = j
                    sentence_copy["obj_type"] = sentence['stanford_ner'][j]
                    sentences_all_possible.append(sentence_copy)

    print("Number of sentences:", len(sentences))
    print("Number of all possible sentences:", len(sentences_all_possible))
    with open(write_filename, "w") as write_file:
        # json.dump(sentences_all_possible, write_file, separators=(',', ':'))
        json.dump(sentences, write_file, separators=(',', ':'))


if __name__ == '__main__':
    pre_process("./curated_emm_data_without_gold.json", "./gold_test.json")
