import cPickle as pickle
import numpy as np
import codecs as cd
import os,re,operator,argparse
from twtokenize import tokenizeRawTweetText as tokenize
from twtokenize import url,AtMention

def readinfo(fname):
    with cd.open(fname, 'rb') as f:
        info=pickle.load(f)
    return info

def load_sowe(fname,infofile):
    info=readinfo(infofile)
    word_idx_map=info['vocab']
    wordVectors = np.load(fname)
    embs = {}
    for word in word_idx_map:
        score=wordVectors[word_idx_map[word]]
        embs[word] = score[1]-score[0]  
    embs['<unk>']=0.
    return embs

def load_sowe_2param(fname,infofile):
    info=readinfo(infofile)
    word_idx_map=info['vocab']
    wordVectors = np.load(fname)
    embs = {}
    for word in word_idx_map:
        score=wordVectors[word_idx_map[word]]
        embs[word] = [score[1],score[0]]  
    embs['<unk>']=[0,0]
    return embs

def wlexicon(wfile,lexicons):
    sorted_lexicons = sorted(lexicons.items(), key=operator.itemgetter(1),reverse=True)
    with cd.open(wfile,'wb',encoding='utf8') as f:
        for (k,v) in sorted_lexicons:
#             k = k.encode('latin1').decode('utf-8', 'ignore')
            nl = k + u'\t'+ str(v) +u'\n'
            f.write(nl)

def wlexicon_2param(wfile,lexicons):
    sorted_lexicons = sorted(lexicons.items(), key=operator.itemgetter(1),reverse=True)
    with cd.open(wfile,'wb',encoding='utf8') as f:
        for (k,v) in sorted_lexicons:
#             k = k.encode('latin1').decode('utf-8', 'ignore')
            nl = k + u'\t'+ str(v[0]) +u'\t'+str(v[1])+u'\n'
            f.write(nl)


parser = argparse.ArgumentParser(description='...')
parser.add_argument('langue', type=str, help='input en, vi, zh, ar')
parser.add_argument('savingType', type=str, help='input SS for saving Sentiment Scores, PMI for saving Pointwise Mutual Infomation')

args = parser.parse_args()

if args.langue not in ['en', 'vi', 'ar', 'zh']:
        raise ValueError("kind must be 'en', 'vi', 'ar' or 'zh'")

if args.savingType not in ['SS', 'PMI']:
        raise ValueError("kind must be 'SS' or 'PMI'")

lang = args.langue
savingType = args.savingType

lexicon_lang = "mylexicon-"+lang
lexicon_lang_file = lang+"-lexicons-"+savingType+".txt"

if not os.path.exists("./saved_lexicon"): os.mkdir("./saved_lexicon")


lexiconfile= os.path.join("./data","lexicons",lexicon_lang,"epoch_5Words_current.npy")
infofile= os.path.join("./data","lexicons",lexicon_lang,"info.tw")
wfile = os.path.join("./saved_lexicon", lexicon_lang_file)

if(savingType == 'SS'):
    lexicons = load_sowe(lexiconfile,infofile)
    wlexicon(wfile,lexicons)

if(savingType == 'PMI'):
    lexicons = load_sowe_2param(lexiconfile,infofile)
    wlexicon_2param(wfile,lexicons)