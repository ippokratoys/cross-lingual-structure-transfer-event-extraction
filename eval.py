"""
Run evaluation with saved models.
"""
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
for i, b in enumerate(batch_iter):
    preds, probs, _ = trainer.predict(b)
    # uncoment if you want to see examples
    # for j, pred in enumerate(preds):
    #     if pred != 0:
    #         print("----------")
    #         index = batch.batch_size * i + j
    #         raw_data = batch.raw_data[index]
    #         print(index)
    #         print("Returned: ", id2label[pred])
    #         print("Expected: ", raw_data['relation'])
    #         print(raw_data['sentence'])
    #         print(raw_data['id'])
    #         print("----------")
    predictions += preds
    all_probs += probs

predictions = [id2label[p] for p in predictions]
p, r, f1 = scorer.score(batch.gold(), predictions, verbose=True)
print("{} set evaluate result: {:.2f}\t{:.2f}\t{:.2f}".format(args.dataset, p, r, f1))

print("Evaluation ended.")
