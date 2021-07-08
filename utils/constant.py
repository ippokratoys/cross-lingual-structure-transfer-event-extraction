"""
Define constants.
"""
EMB_INIT_RANGE = 1.0

# vocab
PAD_TOKEN = '<PAD>'
PAD_ID = 0
UNK_TOKEN = '<UNK>'
UNK_ID = 1

VOCAB_PREFIX = [PAD_TOKEN, UNK_TOKEN]

# hard-coded mappings from fields to ids
SUBJ_NER_TO_ID = {PAD_TOKEN: 0, UNK_TOKEN: 1, 'INTJ': 2, 'NUM': 3, 'NOUN': 4, 'PART': 5, 'VERB': 6, 'X': 7, 'ADJ': 8,
                  'ADV': 9, 'DET': 10, 'SYM': 11, 'PUNCT': 12, 'ADP': 13, 'PROPN': 14, 'CCONJ': 15, 'PRON': 16,
                  'SCONJ': 17,
                  'AUX': 18}

OBJ_NER_TO_ID = {PAD_TOKEN: 0, UNK_TOKEN: 1, 'B-GPE': 2, 'B-LOC': 3, 'O': 4, 'E-TIME': 5, 'E-DATE': 6, 'S-ORDINAL': 7,
                 'S-PRODUCT': 8, 'B-WORK_OF_ART': 9, 'E-EVENT': 10, 'B-DATE': 11, 'S-TIME': 12, 'S-WORK_OF_ART': 13,
                 'E-PRODUCT': 14, 'S-FAC': 15, 'B-TIME': 16, 'E-GPE': 17, 'B-MONEY': 18, 'E-CARDINAL': 19, 'I-FAC': 20,
                 'E-LAW': 21, 'E-WORK_OF_ART': 22, 'E-ORG': 23, 'E-MONEY': 24, 'E-PERCENT': 25, 'I-PERCENT': 26,
                 'S-LAW': 27, 'B-NORP': 28, 'I-WORK_OF_ART': 29, 'B-QUANTITY': 30, 'B-EVENT': 31, 'E-NORP': 32,
                 'B-ORG': 33,
                 'B-PERSON': 34, 'S-GPE': 35, 'I-PERSON': 36, 'B-PERCENT': 37, 'S-DATE': 38, 'S-ORG': 39,
                 'S-LANGUAGE': 40,
                 'I-PRODUCT': 41, 'E-LOC': 42, 'E-PERSON': 43, 'I-ORG': 44, 'S-PERSON': 45, 'S-NORP': 46, 'I-NORP': 47,
                 'S-EVENT': 48, 'I-LOC': 49, 'I-MONEY': 50, 'B-PRODUCT': 51, 'I-DATE': 52, 'E-FAC': 53, 'B-LAW': 54,
                 'B-FAC': 55, 'I-TIME': 56, 'S-LOC': 57, 'E-QUANTITY': 58, 'S-MONEY': 59, 'S-CARDINAL': 60,
                 'I-EVENT': 61,
                 'B-CARDINAL': 62, 'I-GPE': 63, 'I-QUANTITY': 64, 'I-CARDINAL': 65, 'S-QUANTITY': 66, 'I-LAW': 67}

# update ids
NER_TO_ID = {PAD_TOKEN: 0, UNK_TOKEN: 1, 'B-GPE': 2, 'B-LOC': 3, 'O': 4, 'E-TIME': 5, 'E-DATE': 6, 'S-ORDINAL': 7,
             'S-PRODUCT': 8, 'B-WORK_OF_ART': 9, 'E-EVENT': 10, 'B-DATE': 11, 'S-TIME': 12, 'S-WORK_OF_ART': 13,
             'E-PRODUCT': 14, 'S-FAC': 15, 'B-TIME': 16, 'E-GPE': 17, 'B-MONEY': 18, 'E-CARDINAL': 19, 'I-FAC': 20,
             'E-LAW': 21, 'E-WORK_OF_ART': 22, 'E-ORG': 23, 'E-MONEY': 24, 'E-PERCENT': 25, 'I-PERCENT': 26,
             'S-LAW': 27, 'B-NORP': 28, 'I-WORK_OF_ART': 29, 'B-QUANTITY': 30, 'B-EVENT': 31, 'E-NORP': 32, 'B-ORG': 33,
             'B-PERSON': 34, 'S-GPE': 35, 'I-PERSON': 36, 'B-PERCENT': 37, 'S-DATE': 38, 'S-ORG': 39, 'S-LANGUAGE': 40,
             'I-PRODUCT': 41, 'E-LOC': 42, 'E-PERSON': 43, 'I-ORG': 44, 'S-PERSON': 45, 'S-NORP': 46, 'I-NORP': 47,
             'S-EVENT': 48, 'I-LOC': 49, 'I-MONEY': 50, 'B-PRODUCT': 51, 'I-DATE': 52, 'E-FAC': 53, 'B-LAW': 54,
             'B-FAC': 55, 'I-TIME': 56, 'S-LOC': 57, 'E-QUANTITY': 58, 'S-MONEY': 59, 'S-CARDINAL': 60, 'I-EVENT': 61,
             'B-CARDINAL': 62, 'I-GPE': 63, 'I-QUANTITY': 64, 'I-CARDINAL': 65, 'S-QUANTITY': 66, 'I-LAW': 67}

# update ids
POS_TO_ID = {PAD_TOKEN: 0, UNK_TOKEN: 1, 'INTJ': 2, 'NUM': 3, 'NOUN': 4, 'PART': 5, 'VERB': 6, 'X': 7, 'ADJ': 8,
             'ADV': 9, 'DET': 10, 'SYM': 11, 'PUNCT': 12, 'ADP': 13, 'PROPN': 14, 'CCONJ': 15, 'PRON': 16, 'SCONJ': 17,
             'AUX': 18}

# looks similar (needs update)
DEPREL_TO_ID = {PAD_TOKEN: 0, UNK_TOKEN: 1, 'expl': 2, 'acl': 3, 'obl': 4, 'obl:npmod': 5, 'obl:tmod': 6, 'vocative': 7,
                'nsubj:pass': 8, 'ccomp': 9, 'goeswith': 10, 'amod': 11, 'det': 12, 'conj': 13, 'root': 14,
                'nmod:tmod': 15, 'compound': 16, 'csubj': 17, 'nummod': 18, 'cc:preconj': 19, 'advcl': 20,
                'aux:pass': 21, 'flat': 22, 'obj': 23, 'nmod:npmod': 24, 'mark': 25, 'cc': 26, 'xcomp': 27,
                'parataxis': 28, 'nsubj': 29, 'appos': 30, 'advmod': 31, 'discourse': 32, 'punct': 33, 'list': 34,
                'aux': 35, 'case': 36, 'det:predet': 37, 'iobj': 38, 'nmod:poss': 39, 'acl:relcl': 40, 'nmod': 41,
                'fixed': 42, 'cop': 43, 'compound:prt': 44}

NEGATIVE_LABEL = 'no_relation'

LABEL_TO_ID = {'no_relation': 0, 'manufacture': 1, 'contact': 2, 'government': 3, 'movement': 4, 'disaster': 5,
               'conflict': 6, 'justice': 7, 'artifactexistence': 8, 'inspection': 9, 'personnel': 10, 'transaction': 11,
               'life': 12}

# LABEL_TO_ID = {'no_relation': 0, 'justice.judicialconsequences.extradite': 1, 'life.die.n/a': 2,
#                'life.die.nonviolentdeath': 3,
#                'contact.requestadvise.meet': 4, 'conflict.attack.biologicalchemicalpoisonattack': 5,
#                'contact.collaborate.n/a': 6, 'transaction.transfermoney.purchase': 7,
#                'disaster.accidentcrash.accidentcrash': 8, 'transaction.transferownership.borrowlend': 9,
#                'personnel.startposition.n/a': 10, 'conflict.attack.airstrikemissilestrike': 11,
#                'transaction.transaction.embargosanction': 12, 'manufacture.artifact.createintellectualproperty': 13,
#                'contact.publicstatementinperson.n/a': 14, 'life.die.deathcausedbyviolentevents': 15,
#                'transaction.transfermoney.borrowlend': 16, 'contact.commitmentpromiseexpressintent.n/a': 17,
#                'contact.prevarication.broadcast': 18, 'conflict.yield.retreat': 19,
#                'justice.judicialconsequences.convict': 20, 'movement.transportartifact.receiveimport': 21,
#                'movement.transportperson.bringcarryunload': 22, 'movement.transportperson.grantentryasylum': 23,
#                'personnel.endposition.quitretire': 24, 'movement.transportartifact.smuggleextract': 25,
#                'contact.requestadvise.n/a': 26, 'justice.investigate.n/a': 27,
#                'life.injure.illnessdegradationhungerthirst': 28, 'justice.initiatejudicialprocess.chargeindict': 29,
#                'government.vote.castvote': 30, 'conflict.attack.bombing': 31, 'personnel.startposition.hiring': 32,
#                'transaction.transferownership.embargosanction': 33, 'disaster.fireexplosion.fireexplosion': 34,
#                'justice.judicialconsequences.execute': 35, 'conflict.attack.strangling': 36,
#                'government.formation.n/a': 37, 'transaction.transaction.giftgrantprovideaid': 38,
#                'government.legislate.legislate': 39, 'inspection.sensoryobserve.monitorelection': 40,
#                'conflict.attack.stabbing': 41, 'life.injure.n/a': 42,
#                'inspection.sensoryobserve.inspectpeopleorganization': 43, 'movement.transportartifact.prevententry': 44,
#                'personnel.elect.n/a': 45, 'movement.transportperson.preventexit': 46, 'transaction.transaction.n/a': 47,
#                'transaction.transfermoney.payforservice': 48, 'contact.negotiate.n/a': 49,
#                'government.formation.startgpe': 50, 'transaction.transfermoney.embargosanction': 51,
#                'movement.transportartifact.bringcarryunload': 52, 'movement.transportperson.fall': 53,
#                'contact.commandorder.correspondence': 54, 'justice.investigate.investigatecrime': 55,
#                'contact.prevarication.correspondence': 56, 'contact.prevarication.n/a': 57,
#                'inspection.sensoryobserve.n/a': 58, 'justice.initiatejudicialprocess.trialhearing': 59,
#                'conflict.attack.setfire': 60, 'artifactexistence.damagedestroy.destroy': 61,
#                'movement.transportartifact.nonviolentthrowlaunch': 62, 'contact.prevarication.meet': 63,
#                'movement.transportartifact.sendsupplyexport': 64, 'contact.funeralvigil.n/a': 65,
#                'contact.negotiate.correspondence': 66, 'contact.threatencoerce.correspondence': 67,
#                'contact.commitmentpromiseexpressintent.broadcast': 68, 'contact.discussion.correspondence': 69,
#                'contact.negotiate.meet': 70, 'contact.commandorder.n/a': 71,
#                'life.injure.injurycausedbyviolentevents': 72, 'movement.transportartifact.disperseseparate': 73,
#                'manufacture.artifact.build': 74, 'contact.threatencoerce.meet': 75,
#                'movement.transportartifact.fall': 76, 'government.spy.spy': 77,
#                'life.injure.illnessdegradationphysical': 78, 'government.agreements.n/a': 79,
#                'transaction.transaction.transfercontrol': 80, 'movement.transportperson.disperseseparate': 81,
#                'transaction.transfermoney.n/a': 82, 'contact.discussion.meet': 83,
#                'manufacture.artifact.createmanufacture': 84, 'contact.threatencoerce.broadcast': 85,
#                'transaction.transferownership.giftgrantprovideaid': 86, 'contact.discussion.n/a': 87,
#                'personnel.endposition.n/a': 88, 'conflict.attack.invade': 89, 'movement.transportperson.hide': 90,
#                'contact.commandorder.meet': 91, 'artifactexistence.damagedestroy.n/a': 92,
#                'inspection.sensoryobserve.physicalinvestigateinspect': 93, 'contact.requestadvise.correspondence': 94,
#                'contact.funeralvigil.meet': 95, 'government.formation.mergegpe': 96,
#                'contact.commandorder.broadcast': 97, 'contact.mediastatement.n/a': 98,
#                'contact.requestadvise.broadcast': 99, 'contact.mediastatement.broadcast': 100,
#                'contact.collaborate.meet': 101, 'artifactexistence.damagedestroy.damage': 102,
#                'transaction.transferownership.purchase': 103, 'government.vote.violationspreventvote': 104,
#                'justice.arrestjaildetain.arrestjaildetain': 105, 'conflict.attack.firearmattack': 106,
#                'government.agreements.acceptagreementcontractceasefire': 107,
#                'movement.transportartifact.grantentry': 108, 'contact.publicstatementinperson.broadcast': 109,
#                'manufacture.artifact.n/a': 110, 'transaction.transfermoney.giftgrantprovideaid': 111,
#                'contact.collaborate.correspondence': 112, 'conflict.attack.stealrobhijack': 113,
#                'justice.judicialconsequences.n/a': 114, 'conflict.demonstrate.n/a': 115,
#                'movement.transportartifact.preventexit': 116, 'justice.initiatejudicialprocess.n/a': 117,
#                'contact.commitmentpromiseexpressintent.meet': 118, 'conflict.attack.n/a': 119,
#                'government.agreements.rejectnullifyagreementcontractceasefire': 120, 'contact.threatencoerce.n/a': 121,
#                'government.agreements.violateagreement': 122, 'movement.transportperson.evacuationrescue': 123,
#                'conflict.demonstrate.marchprotestpoliticalgathering': 124, 'conflict.yield.n/a': 125,
#                'personnel.elect.winelection': 126, 'conflict.attack.selfdirectedbattle': 127,
#                'movement.transportperson.smuggleextract': 128, 'conflict.yield.surrender': 129,
#                'movement.transportartifact.hide': 130, 'transaction.transferownership.n/a': 131,
#                'movement.transportperson.prevententry': 132, 'movement.transportperson.n/a': 133,
#                'movement.transportartifact.n/a': 134, 'conflict.attack.hanging': 135, 'government.vote.n/a': 136,
#                'contact.commitmentpromiseexpressintent.correspondence': 137, 'movement.transportperson.selfmotion': 138,
#                'personnel.endposition.firinglayoff': 139}

INFINITY_NUMBER = 1e12
