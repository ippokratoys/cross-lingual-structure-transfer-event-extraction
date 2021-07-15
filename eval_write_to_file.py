"""
Run evaluation with saved models.
"""
import json
import random
import argparse

import numpy as np
from torch import nn
from tqdm import tqdm
import torch

from data.loader import DataLoader
from model.trainer import GCNTrainer
from utils import torch_utils, scorer, constant, helper
from utils.vocab import Vocab

parser = argparse.ArgumentParser()
parser.add_argument('model_dir', type=str, help='Directory of the model.')
parser.add_argument('--model', type=str, default='best_model.pt', help='Name of the model file.')
parser.add_argument('--data_dir', type=str, default='dataset/tacred')
parser.add_argument('--results', type=str, default='out.json')
parser.add_argument('--dataset', type=str, default='test', help="Evaluate on dev or test.")
parser.add_argument('--vocab_file', type=str, default='',
                    help="The vocab file depending on the language dataset language (the result of prepare_vocab)")

parser.add_argument('--seed', type=int, default=1234)
parser.add_argument('--cuda', type=bool, default=torch.cuda.is_available())
parser.add_argument('--cpu', action='store_true')
args = parser.parse_args()

torch.manual_seed(args.seed)
random.seed(1234)
if args.cpu:
    args.cuda = False
elif args.cuda:
    torch.cuda.manual_seed(args.seed)

# load opt
model_file = args.model_dir + '/' + args.model
print("Loading model from {}".format(model_file))
opt = torch_utils.load_config(model_file)

# load vocab
if args.vocab_file:
    opt['vocab_dir'] = args.vocab_file
    vocab_file = args.vocab_file + '/vocab.pkl'
else:
    vocab_file = args.model_dir + '/vocab.pkl'

trainer = GCNTrainer(opt)
trainer.load(model_file)

print(vocab_file)
vocab = Vocab(vocab_file, load=True)
# skipped due to different language
# assert opt['vocab_size'] == vocab.size, "Vocab size must match that in the saved model."

# Update gcn vocab embeddings for the target language
target_lang_emb = nn.Embedding(vocab.size, opt['emb_dim'], padding_idx=constant.PAD_ID)
emb_file = opt['vocab_dir'] + '/embedding.npy'
emb_matrix = np.load(emb_file)
emb_matrix = torch.from_numpy(emb_matrix)
target_lang_emb.weight.data.copy_(emb_matrix)
if args.cuda:
    target_lang_emb = target_lang_emb.cuda()
trainer.model.gcn_model.gcn.emb = target_lang_emb

# load data
opt['data_dir'] = args.data_dir
opt['dataset'] = args.dataset
data_file = opt['data_dir'] + '/{}.json'.format(args.dataset)
print("Loading data from {} with batch size {}...".format(data_file, opt['batch_size']))
batch = DataLoader(data_file, opt['batch_size'], opt, vocab, evaluation=True)

helper.print_config(opt)
label2id = constant.LABEL_TO_ID
id2label = dict([(v, k) for k, v in label2id.items()])

predictions = []
all_probs = []
batch_iter = tqdm(batch)

results = []
for i, b in enumerate(batch_iter):
    preds, probs, _ = trainer.predict(b)
    for j, pred in enumerate(preds):
        index = batch.batch_size * i + j
        raw_data = batch.raw_data[index]

        label = id2label[pred]
        if label != 'no_relation':
            results.append({
                "id": raw_data['id'],
                "event": id2label[pred],
                "event_trigger_start": raw_data['obj_start'],
                "event_trigger_end": raw_data['obj_end'],
                "argument_start": raw_data['subj_start'],
                "argument_end": raw_data['subj_end']
            })

    predictions += preds
    all_probs += probs

final_results = []
ids = [result.id for result in results]
for id in ids:
    events_for_id = [result.event for result in results if result.id == id]
    if events_for_id.count('no_relation') == len(events_for_id):
        final_results.append({
            "id": id,
            "event": "no_event"
        })
    else:
        final_results.append({
            "id": id,
            "event": max(events_for_id, key=events_for_id.count)
        })

with open(args.results, "w") as write_file:
    json.dump(final_results, write_file, separators=(',', ':'))

predictions = [id2label[p] for p in predictions]
p, r, f1 = scorer.score(batch.gold(), predictions, verbose=True)
print("{} set evaluate result: {:.2f}\t{:.2f}\t{:.2f}".format(args.dataset, p, r, f1))

print("Evaluation ended.")
