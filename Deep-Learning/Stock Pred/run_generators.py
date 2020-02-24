from generators.data_generator import data_generator
from generators.svo_generator import svo_generator
from generators.svo_embedding_generator import svo_embedding_generator
import os

path = os.getcwd()+'/data/'
data_generator.extract_news_titles(path)
svo_generator.extract_relation_triples(path)
svo_embedding_generator.svo_to_word_embedding(path)

print('Preprocess Complete!')
