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
SUBJ_NER_TO_ID = {PAD_TOKEN: 0, UNK_TOKEN: 1, 'ORGANIZATION': 2, 'PERSON': 3}

OBJ_NER_TO_ID = {PAD_TOKEN: 0, UNK_TOKEN: 1, 'PERSON': 2, 'ORGANIZATION': 3, 'DATE': 4, 'NUMBER': 5, 'TITLE': 6,
                 'COUNTRY': 7, 'LOCATION': 8, 'CITY': 9, 'MISC': 10, 'STATE_OR_PROVINCE': 11, 'DURATION': 12,
                 'NATIONALITY': 13, 'CAUSE_OF_DEATH': 14, 'CRIMINAL_CHARGE': 15, 'RELIGION': 16, 'URL': 17,
                 'IDEOLOGY': 18}

# update ids
NER_TO_ID = {PAD_TOKEN: 0, UNK_TOKEN: 1, 'O': 2, 'PERSON': 3, 'ORGANIZATION': 4, 'LOCATION': 5, 'DATE': 6, 'NUMBER': 7,
             'MISC': 8, 'DURATION': 9, 'MONEY': 10, 'PERCENT': 11, 'ORDINAL': 12, 'TIME': 13, 'SET': 14}

# update ids
POS_TO_ID = {PAD_TOKEN: 0, UNK_TOKEN: 1, 'NNP': 2, 'NN': 3, 'IN': 4, 'DT': 5, ',': 6, 'JJ': 7, 'NNS': 8, 'VBD': 9,
             'CD': 10, 'CC': 11, '.': 12, 'RB': 13, 'VBN': 14, 'PRP': 15, 'TO': 16, 'VB': 17, 'VBG': 18, 'VBZ': 19,
             'PRP$': 20, ':': 21, 'POS': 22, '\'\'': 23, '``': 24, '-RRB-': 25, '-LRB-': 26, 'VBP': 27, 'MD': 28,
             'NNPS': 29, 'WP': 30, 'WDT': 31, 'WRB': 32, 'RP': 33, 'JJR': 34, 'JJS': 35, '$': 36, 'FW': 37, 'RBR': 38,
             'SYM': 39, 'EX': 40, 'RBS': 41, 'WP$': 42, 'PDT': 43, 'LS': 44, 'UH': 45, '#': 46}

# looks similar (needs update)
DEPREL_TO_ID = {PAD_TOKEN: 0, UNK_TOKEN: 1, 'punct': 2, 'compound': 3, 'case': 4, 'nmod': 5, 'det': 6, 'nsubj': 7,
                'amod': 8, 'conj': 9, 'dobj': 10, 'ROOT': 11, 'cc': 12, 'nmod:poss': 13, 'mark': 14, 'advmod': 15,
                'appos': 16, 'nummod': 17, 'dep': 18, 'ccomp': 19, 'aux': 20, 'advcl': 21, 'acl:relcl': 22, 'xcomp': 23,
                'cop': 24, 'acl': 25, 'auxpass': 26, 'nsubjpass': 27, 'nmod:tmod': 28, 'neg': 29, 'compound:prt': 30,
                'mwe': 31, 'parataxis': 32, 'root': 33, 'nmod:npmod': 34, 'expl': 35, 'csubj': 36, 'cc:preconj': 37,
                'iobj': 38, 'det:predet': 39, 'discourse': 40, 'csubjpass': 41}

NEGATIVE_LABEL = 'no_relation'

LABEL_TO_ID = {'no_relation': 0, 'justice.judicialconsequences.extradite': 1, 'life.die.n/a': 2,
               'life.die.nonviolentdeath': 3,
               'contact.requestadvise.meet': 4, 'conflict.attack.biologicalchemicalpoisonattack': 5,
               'contact.collaborate.n/a': 6, 'transaction.transfermoney.purchase': 7,
               'disaster.accidentcrash.accidentcrash': 8, 'transaction.transferownership.borrowlend': 9,
               'personnel.startposition.n/a': 10, 'conflict.attack.airstrikemissilestrike': 11,
               'transaction.transaction.embargosanction': 12, 'manufacture.artifact.createintellectualproperty': 13,
               'contact.publicstatementinperson.n/a': 14, 'life.die.deathcausedbyviolentevents': 15,
               'transaction.transfermoney.borrowlend': 16, 'contact.commitmentpromiseexpressintent.n/a': 17,
               'contact.prevarication.broadcast': 18, 'conflict.yield.retreat': 19,
               'justice.judicialconsequences.convict': 20, 'movement.transportartifact.receiveimport': 21,
               'movement.transportperson.bringcarryunload': 22, 'movement.transportperson.grantentryasylum': 23,
               'personnel.endposition.quitretire': 24, 'movement.transportartifact.smuggleextract': 25,
               'contact.requestadvise.n/a': 26, 'justice.investigate.n/a': 27,
               'life.injure.illnessdegradationhungerthirst': 28, 'justice.initiatejudicialprocess.chargeindict': 29,
               'government.vote.castvote': 30, 'conflict.attack.bombing': 31, 'personnel.startposition.hiring': 32,
               'transaction.transferownership.embargosanction': 33, 'disaster.fireexplosion.fireexplosion': 34,
               'justice.judicialconsequences.execute': 35, 'conflict.attack.strangling': 36,
               'government.formation.n/a': 37, 'transaction.transaction.giftgrantprovideaid': 38,
               'government.legislate.legislate': 39, 'inspection.sensoryobserve.monitorelection': 40,
               'conflict.attack.stabbing': 41, 'life.injure.n/a': 42,
               'inspection.sensoryobserve.inspectpeopleorganization': 43, 'movement.transportartifact.prevententry': 44,
               'personnel.elect.n/a': 45, 'movement.transportperson.preventexit': 46, 'transaction.transaction.n/a': 47,
               'transaction.transfermoney.payforservice': 48, 'contact.negotiate.n/a': 49,
               'government.formation.startgpe': 50, 'transaction.transfermoney.embargosanction': 51,
               'movement.transportartifact.bringcarryunload': 52, 'movement.transportperson.fall': 53,
               'contact.commandorder.correspondence': 54, 'justice.investigate.investigatecrime': 55,
               'contact.prevarication.correspondence': 56, 'contact.prevarication.n/a': 57,
               'inspection.sensoryobserve.n/a': 58, 'justice.initiatejudicialprocess.trialhearing': 59,
               'conflict.attack.setfire': 60, 'artifactexistence.damagedestroy.destroy': 61,
               'movement.transportartifact.nonviolentthrowlaunch': 62, 'contact.prevarication.meet': 63,
               'movement.transportartifact.sendsupplyexport': 64, 'contact.funeralvigil.n/a': 65,
               'contact.negotiate.correspondence': 66, 'contact.threatencoerce.correspondence': 67,
               'contact.commitmentpromiseexpressintent.broadcast': 68, 'contact.discussion.correspondence': 69,
               'contact.negotiate.meet': 70, 'contact.commandorder.n/a': 71,
               'life.injure.injurycausedbyviolentevents': 72, 'movement.transportartifact.disperseseparate': 73,
               'manufacture.artifact.build': 74, 'contact.threatencoerce.meet': 75,
               'movement.transportartifact.fall': 76, 'government.spy.spy': 77,
               'life.injure.illnessdegradationphysical': 78, 'government.agreements.n/a': 79,
               'transaction.transaction.transfercontrol': 80, 'movement.transportperson.disperseseparate': 81,
               'transaction.transfermoney.n/a': 82, 'contact.discussion.meet': 83,
               'manufacture.artifact.createmanufacture': 84, 'contact.threatencoerce.broadcast': 85,
               'transaction.transferownership.giftgrantprovideaid': 86, 'contact.discussion.n/a': 87,
               'personnel.endposition.n/a': 88, 'conflict.attack.invade': 89, 'movement.transportperson.hide': 90,
               'contact.commandorder.meet': 91, 'artifactexistence.damagedestroy.n/a': 92,
               'inspection.sensoryobserve.physicalinvestigateinspect': 93, 'contact.requestadvise.correspondence': 94,
               'contact.funeralvigil.meet': 95, 'government.formation.mergegpe': 96,
               'contact.commandorder.broadcast': 97, 'contact.mediastatement.n/a': 98,
               'contact.requestadvise.broadcast': 99, 'contact.mediastatement.broadcast': 100,
               'contact.collaborate.meet': 101, 'artifactexistence.damagedestroy.damage': 102,
               'transaction.transferownership.purchase': 103, 'government.vote.violationspreventvote': 104,
               'justice.arrestjaildetain.arrestjaildetain': 105, 'conflict.attack.firearmattack': 106,
               'government.agreements.acceptagreementcontractceasefire': 107,
               'movement.transportartifact.grantentry': 108, 'contact.publicstatementinperson.broadcast': 109,
               'manufacture.artifact.n/a': 110, 'transaction.transfermoney.giftgrantprovideaid': 111,
               'contact.collaborate.correspondence': 112, 'conflict.attack.stealrobhijack': 113,
               'justice.judicialconsequences.n/a': 114, 'conflict.demonstrate.n/a': 115,
               'movement.transportartifact.preventexit': 116, 'justice.initiatejudicialprocess.n/a': 117,
               'contact.commitmentpromiseexpressintent.meet': 118, 'conflict.attack.n/a': 119,
               'government.agreements.rejectnullifyagreementcontractceasefire': 120, 'contact.threatencoerce.n/a': 121,
               'government.agreements.violateagreement': 122, 'movement.transportperson.evacuationrescue': 123,
               'conflict.demonstrate.marchprotestpoliticalgathering': 124, 'conflict.yield.n/a': 125,
               'personnel.elect.winelection': 126, 'conflict.attack.selfdirectedbattle': 127,
               'movement.transportperson.smuggleextract': 128, 'conflict.yield.surrender': 129,
               'movement.transportartifact.hide': 130, 'transaction.transferownership.n/a': 131,
               'movement.transportperson.prevententry': 132, 'movement.transportperson.n/a': 133,
               'movement.transportartifact.n/a': 134, 'conflict.attack.hanging': 135, 'government.vote.n/a': 136,
               'contact.commitmentpromiseexpressintent.correspondence': 137, 'movement.transportperson.selfmotion': 138,
               'personnel.endposition.firinglayoff': 139}

INFINITY_NUMBER = 1e12
