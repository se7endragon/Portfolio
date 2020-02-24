import numpy as np
import pickle

class svo_embedding_generator(object):
    def svo_to_word_embedding(path):
        #Load SVO Dictionary
        with open(path+'svo_dict.pickle', 'rb') as handle:
            svo_dict = pickle.load(handle)

        #Dictionary for pre-trained word embedding Glove
        word_embedding = {}
        with open(path+'Glove.txt') as f:
            for chunk in f:
                tmp = np.array(chunk.split(" "))
                tmp[-1] = tmp[-1][:-1]
                key = tmp[0]
                val = np.float_(tmp[1:])
                word_embedding[key] = val

        #NL <-> Word Embedding for extracted SVO_triples
        svo_dict_embed = {}
        for k,v in svo_dict.items():
            #day_svo = np.empty((len(svo_dict[k]),3))
            day_svo = []#collection of news triples daily
            for triple in v: #for each news within a day
                svo_embed = [] #collection of s,v,o vectors per news
                for word in triple: #for each word in a news triple
                    temp_embed = [] #collection of temporary word vectors per extraction
                    if "'" in word:
                        word = word.replace("'","")
                    if " " in word:
                        splitted = word.split(" ")
                        for split_word in splitted:
                            if split_word in word_embedding:
                                temp_embed.append(word_embedding[split_word])
                        if len(temp_embed) > 1:
                            svo_embed.append(np.mean(temp_embed,axis=0))
                        elif len(temp_embed) == 1:
                            svo_embed.append(temp_embed)
                    else:
                        if word in word_embedding:
                            svo_embed.append(word_embedding[word])
                        else:
                            break
                if len(svo_embed) == 3:
                    day_svo.append(svo_embed)
            svo_dict_embed[k]= day_svo

        with open(path+'svo_dict_embed.pickle','wb') as handle:
            pickle.dump(svo_dict_embed,handle,protocol=pickle.HIGHEST_PROTOCOL)
