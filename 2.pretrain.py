import sys,re,os, argparse
from collections import defaultdict
import codecs as cd
from twtokenize import tokenizeRawTweetText as tokenize
from twtokenize import url,AtMention
import cPickle as pickle
import numpy as np



usernorm=re.compile(unicode(AtMention.decode('utf-8')), re.UNICODE)
urlnorm=re.compile(unicode(url.decode('utf-8')), re.UNICODE)

#-----------------------------------------------------------------------------#   
#           Stream each line of training data (format: label tweet)           # 
#-----------------------------------------------------------------------------# 
class streamtw(object):
    def __init__(self, fname):
        self.fname = fname
    def __iter__(self):
        with cd.open(self.fname,'rb', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().lower().split()
                if len(parts)>=2:
                    y = parts[0]
                    tw=' '.join(parts[1:])
#                    x = tokenize(tw.decode('latin1')) # decoding in Latin1 for Arabic
                    x = tokenize(tw)
                    x=u' '.join(x)
                    yield x,y
#-----------------------------------------------------------------------------#   
# Process training data (tokenize, substitute username, http, emoticons,...)  # 
#-----------------------------------------------------------------------------#                     
class Vocab:        
    @staticmethod
    def create_vocabulary(fname,sentences,cutoff,metafile):
        vocab = defaultdict(float)
        max_l=-np.inf
        c=0
        
        num_lines = float(sum(1 for line in open(metafile)))
        
        with cd.open(fname,'wb',encoding='utf-8') as f:
            for sent in sentences:
                line,label = sent 
                words = Vocab.process_line(line)
                for word in words:
                    vocab[word] += 1
                if max_l<=len(words):
                    max_l=len(words)
                nline=label+u' '+u' '.join(words)+u'\n'
                f.write(nline)
                c+=1
                if(c%100 == 0):
                    cent = float(c/num_lines)
                    sys.stdout.write('\r'  + '['+ '#'*(int(cent*100)) + '.'*(int(100 - cent*100)) + ']' + str(float(round((cent*100), 1))) + '% finished.\t\tVocab progress: readed ' + str(c) + ' tweets')
                    sys.stdout.flush()
                    
        lst = [u"<unk>"]+[ x for x, y in vocab.iteritems() if y > cutoff ]
        vocabx = dict([ (y,x) for x,y in enumerate(lst) ])
        info={}
        info['vocab']=vocabx
        info['max_l']=max_l
        info['nosent']=c
        sys.stdout.write('\r'+' '*200)
        sys.stdout.write('\rCorpus has ' + str(len(vocabx)) + ' unique words, '+str(c)+' sentences with max length '+str(max_l))
        sys.stdout.flush()
        return info

    @staticmethod
    def process_line(line):
        line=re.sub(url,u'<url>',line)
        line=re.sub(AtMention,u'<user>',line)
        
        pos=[u':)',u': )',u':-)',u':D',u'=)']
        neg=[u':(',u': (',u':-(']
        emoti=pos+neg
        for emo in emoti:
            line=line.replace(emo,u'')
        
        return line.split()
        
        
    @staticmethod
    def save(fname,vocab):
        with cd.open(fname, 'wb') as f:
            pickle.dump(vocab, f, protocol=pickle.HIGHEST_PROTOCOL)
        print  "Finish saving the vocabulary file"



parser = argparse.ArgumentParser(description='...')
parser.add_argument('langue', type=str, help='input en, vi, zh, ar')

args = parser.parse_args()

if args.langue not in ['en', 'vi', 'ar', 'zh']:
        raise ValueError("kind must be 'en', 'vi', 'ar' or 'zh'")

lang = args.langue

data_lang = lang+"-data"

metafile= os.path.join("./train_data",data_lang,"raw","metatweets")
infofile= os.path.join("./train_data",data_lang,"info.tw")
processfile=os.path.join("./train_data",data_lang,"process.tw")

sentences = streamtw(metafile)
info = Vocab.create_vocabulary(processfile,sentences,5, metafile)
Vocab.save(infofile,info)