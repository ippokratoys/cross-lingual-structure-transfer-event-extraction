"""
Run inference with saved models.
"""
import argparse
import random

import torch
from tqdm import tqdm

from data.loader import DataLoader
from datapreprocessing.transform_data import parse_single
from model.trainer import GCNTrainer
from utils import torch_utils, constant
from utils.vocab import Vocab

parser = argparse.ArgumentParser()
parser.add_argument('model_dir', type=str, help='Directory of the model.')
parser.add_argument('--model', type=str, default='best_model.pt', help='Name of the model file.')
parser.add_argument('--data_dir', type=str, default='dataset/tacred')
parser.add_argument('--dataset', type=str, default='test', help="Evaluate on dev or test.")

parser.add_argument('--seed', type=int, default=1234)
parser.add_argument('--cuda', type=bool, default=torch.cuda.is_available())
parser.add_argument('--cpu', action='store_true')
parser.add_argument('--lang', default="en")
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
trainer = GCNTrainer(opt)
trainer.load(model_file)

# load vocab
vocab_file = args.model_dir + '/vocab.pkl'
vocab = Vocab(vocab_file, load=True)
assert opt['vocab_size'] == vocab.size, "Vocab size must match that in the saved model."

# write data to temp file in order to avoid re-writing

text = input("Enter your value: ")
# text = "Let's go to the mall. Today or tomorrow somithing good (or bad) will take place. Maybe not, we move on"
write_file = opt['data_dir'] + '/{}.json'.format("temp")
parse_single(text, write_file, args.lang)

# load data
batch = DataLoader(write_file, opt['batch_size'], opt, vocab, evaluation=True)

label2id = constant.LABEL_TO_ID
id2label = dict([(v, k) for k, v in label2id.items()])

predictions = []
all_probs = []
batch_iter = tqdm(batch)
for i, b in enumerate(batch_iter):
    preds, probs, _ = trainer.predict(b)
    predictions += preds
    all_probs += probs

predictions = [id2label[p] for p in predictions]
for index, prediction in enumerate(predictions):
    print(prediction, batch.raw_data[index]['sentence'], sep="\t\t")
