import spacy
import textacy
import pickle
from collections import defaultdict

class svo_generator(object):
    def extract_relation_triples(path):
        #load news dictionary for svo extraction
        with open(path+'news_dict.pickle', 'rb') as handle:
            news_dict = pickle.load(handle)

        #English Language Model from spacy
        model = 'en_core_web_lg'
        nlp = spacy.load(model)

        #svo dictionary generator in Spacy.Token.span.Span dtype
        #dictionary{str:[(Spacy.Token.span.Span)]}
        svo_dict = {}
        for k,v in news_dict.items():
            tmpList = []
            for value in v:
                doc = nlp(value)
                b = textacy.extract.subject_verb_object_triples(doc)
                svo = list(b)
                if len(svo) > 0:
                    triple = svo[0]
                    tmpList.append(triple)
            svo_dict[k] = tmpList

        #Type conversion from Spacy.Token.span.Span to str
        #dictionary{str:[[str]]}
        svo_dict_str = defaultdict()
        for k,v in svo_dict.items(): #for each day
            dayList = []
            for val in v: # for each news
                dayList.append([val[0].text,val[1].text,val[2].text]) #append each triple list to dayList
            svo_dict_str[k] = dayList

        #save dictionary for later use as svo_dict.pickle
        with open(path+'svo_dict.pickle', 'wb') as handle:
            pickle.dump(svo_dict_str, handle, protocol=pickle.HIGHEST_PROTOCOL)
