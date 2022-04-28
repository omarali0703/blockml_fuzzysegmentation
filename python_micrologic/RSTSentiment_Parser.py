from lib2to3.pgen2.tokenize import generate_tokens
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.corpus import sentiwordnet as swn
from nltk.corpus import wordnet as wn
import nltk
from nltk import word_tokenize, Tree
from nltk.wsd import lesk
from subprocess import Popen, PIPE, run
import os
import docker
import random
HEAVY = (1.5, 0.5)
LIGHT = (1  , 0)

# Vary feature allows for a feature in the array to be evenly distributed. 
# The feature classes variable keeps track of what variables are being selected.
def randomise_sentDS(arr, limit, vary_feature = None, feature_classes_count = None, charlimit=None):
    randomise_buffer = []
    randomised_list = []
    classes_count = {str(i+1)+".0":0 for i in range(feature_classes_count)}
    buffer_counter = 0
    distribution = limit // feature_classes_count
    # print (classes_count)
    if len(arr) <= limit:
        print (f"Randomiser cannot produce a random list of size {limit}. arr value too small!")
        return 

    while buffer_counter < limit:
        check_int = random.randrange(0, len(arr))
        if check_int not in randomise_buffer and classes_count[str(arr[check_int][vary_feature])] < distribution:
            data_length = len(arr[check_int]['reviewText'].split(' '))
            if charlimit and data_length < charlimit:
                randomise_buffer.append(check_int)
                randomised_list.append(arr[check_int])
                buffer_counter += 1
                classes_count[str(arr[check_int][vary_feature])] += 1
            elif charlimit == None:
                randomise_buffer.append(check_int)
                randomised_list.append(arr[check_int])
                buffer_counter += 1
                classes_count[str(arr[check_int][vary_feature])] += 1                
    # print (f"Randomiser has selected {randomised_list}.")
    return randomised_list
def penn_to_wn(tag):
    """
    Convert between the PennTreebank tags to simple Wordnet tags
    """
    if tag.startswith('J'):
        return wn.ADJ
    elif tag.startswith('N'):
        return wn.NOUN
    elif tag.startswith('R'):
        return wn.ADV
    elif tag.startswith('V'):
        return wn.VERB
    return None

# Parser sentence logic approriated from https://srish6.medium.com/sentiment-analysis-using-the-sentiwordnet-lexicon-1a3d8d856a10,
# Parser has been altered to reflect the work in: https://dl.acm.org/doi/pdf/10.1145/2063576.2063730

def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
 

def str_2_usableobj(str_in):
    print ('Converting to tuple...')
    str_in = str_in.replace('ParseTree', '')
    print ("SHOWING TREE")
    print (str_in, type(str_in))
    print ("END SHOWING TREE")
    to_tup = eval(str_in)
    print ('Converted.')

    return to_tup


import re

w = []
def weight_RST(weights, tup_obj, weight=1, weighting_scheme=LIGHT):
    
    print ("Begin Weighting Process....")
    NUC = '[N]'
    SAT = '[S]'
    
    relation = tup_obj[0]
    subtree = tup_obj[1]
    # print (str(subtree[0])+'\n')
    
    relation_type = re.findall(r'\[[a-zA-Z]\]', relation)
    

    if isinstance(subtree[0], str):
        
        # print (relation_type[0]==NUC, relation_type[1]==NUC)
        if relation_type[0] == NUC:
            weights.append ([subtree[0], weight*weighting_scheme[0]])
            # weights.append ([subtree[1], weight*weighting_scheme[0]])
        
        if relation_type[0] == SAT:
            weights.append ([subtree[0], weight*weighting_scheme[1]])
            # weights.append ([subtree[1], weight*weighting_scheme[0]])

    if isinstance(subtree[1], str):
        # print (relation_type[0]==NUC, relation_type[1]==NUC)
        if relation_type[1] == NUC:
            # weights.append ([subtree[0], weight*weighting_scheme[0]])
            weights.append ([subtree[1], weight*weighting_scheme[0]])
        if relation_type[1] == SAT:
            # weights.append ([subtree[0], weight*weighting_scheme[0]])
            weights.append ([subtree[1], weight*weighting_scheme[1]])

    if isinstance(subtree[1], tuple):
        if relation_type[1] == NUC:
            # weight_RST(weights, subtree[0], weight*weighting_scheme[0])
            weight_RST(weights, subtree[1], weight*weighting_scheme[0])
        if relation_type[1] == SAT:
            # weight_RST(weights, subtree[0], weight*weighting_scheme[0])
            weight_RST(weights, subtree[1], weight*weighting_scheme[1])
    
    if isinstance(subtree[0], tuple):
        if relation_type[0] == NUC:
            weight_RST(weights, subtree[0], weight*weighting_scheme[0])
            # weight_RST(weights, subtree[1], weight*weighting_scheme[0])
        if relation_type[0] == SAT:
            weight_RST(weights, subtree[0], weight*weighting_scheme[1])
            # weight_RST(weights, subtree[1], weight*weighting_scheme[1])
    print ("FINISHED Weighting Process....")

        
def get_rst_tree(input_dir, edu_dir=None, cuts_dir=None):
    file_name = input_dir
    root_dir = os.path.dirname(os.path.dirname(__file__))
    # input_dir = os.path.join(input_dir, '..')
    # input_dir = os.path.join(root_dir, f"dependencies/hilda-docker/{file_name}")
    # edu_dir = os.path.join(root_dir, f"dependencies/hilda-docker/{edu_dir}")
    # cuts_dir = os.path.join(root_dir, f"dependencies/hilda-docker/{cuts_dir}")
    print (file_name, input_dir, edu_dir, cuts_dir)
   
    cmd = f"docker run -v /tmp:/tmp -ti hilda {file_name}";
    if edu_dir:
        cmd = f"docker run -v /tmp:/tmp -ti hilda {file_name} {edu_dir} {cuts_dir}";

    p = Popen(cmd.split(), stdout=PIPE, shell=False)
    generated_tree, err = p.communicate()
    p_status = p.wait()
    
    print ("FINISHED GENERATING FROM CMD LINE.")
    print (generated_tree)
    generated_tree = generated_tree.decode('utf-8')
    generated_tree = str_2_usableobj(generated_tree)
    return generated_tree
    # print (generated_tree.leaves())

# x = '''ParseTree(
#     'Contrast[S][N]',
#     ['Not much to write about here ,',0.5
#     ParseTree('Elaboration[N][S]',1.5
#         ["but it does exactly what it 's supposed to .",
#         ParseTree('Elaboration[N][S]',
#             [ParseTree('Elaboration[N][S]', [
#                 'filters out the pop sounds .',
#                 'now my recordings are much more crisp .']),
#             ParseTree('Elaboration[N][S]',
#                 ['it is one of the lowest prices pop filters on amazon so might as well buy it ,',
#                 'they honestly work the same despite their pricing ,'])])])])'''

# # x = '''ParseTree('Contrast[S][N]', ['Not much to write about here ,', ParseTree('Elaboration[N][S]',["but it does exactly what it 's supposed to .", ParseTree('Elaboration[N][S]',[ParseTree('Elaboration[N][S]', ['filters out the pop sounds .','now my recordings are much more crisp .']),ParseTree('Elaboration[N][S]',['it is one of the lowest prices pop filters on amazon so might as well buy it ,', 'they honestly work the same despite their pricing ,'])])])])'''
# # x = '''ParseTree('Elaboration[N][S]', [ParseTree('Elaboration[N][S]', [ParseTree('Elaboration[N][S]', [ParseTree('same-unit[N][N]', [ParseTree('Elaboration[N][S]', ['The primary job of this device is to block the breath', 'that would otherwise produce a popping sound ,']), ParseTree('Enablement[N][S]', ['while allowing your voice', 'to pass through with no noticeable reduction of volume or high frequencies .'])]), ParseTree('Joint[N][N]', ['The double cloth filter blocks the pops', 'and lets the voice through with no coloration .'])]), ParseTree('Elaboration[N][S]', ['The metal clamp mount attaches to the mike stand secure enough', 'to keep it attached .'])]), ParseTree('Elaboration[N][S]', ['The goose neck needs a little coaxing to stay', 'where you put it .'])])'''
# # x = str_2_usableobj(x)
# # [['The goose neck needs a little coaxing to stay', 2.25], ['where you put it .', 0.75], ['The metal clamp mount attaches to the mike stand secure enough', 2.25], ['to keep it attached .', 0.75], ['The double cloth filter blocks the pops', 2.25], ['and lets the voice through with no coloration .', 2.25], ['while allowing your voice', 0.75], ['to pass through with no noticeable reduction of volume or high frequencies .', 0.25], ['The primary job of this device is to block the breath', 1.5], ['that would otherwise produce a popping sound ,', 0.5]]
# print (x)
# weight_RST(w, x)
# print (w)
# weight_RST()
def parse_sentence(sentence, rst=False):
    token = nltk.word_tokenize(sentence)
    after_tagging = nltk.pos_tag(token)

    sentiment = 0.0
    tokens_count = 0
    lemmatizer = WordNetLemmatizer()
    for word, tag in after_tagging:
        wn_tag = penn_to_wn(tag)
        if wn_tag not in (wn.NOUN, wn.ADJ, wn.ADV):
            continue

        lemma = lemmatizer.lemmatize(word, pos=wn_tag)
        if not lemma:
            continue

        synsets = wn.synsets(lemma, pos=wn_tag)
        if not synsets:
            continue

        # Take the first sense, the most common
        if len(synsets) <= 1:
            synset = synsets[0]
        
        swn_synset = swn.senti_synset(synset.name())
        # print(swn_synset)

        sentiment += swn_synset.pos_score() - swn_synset.neg_score()
        tokens_count += 1
   
    sentiment = sentiment/tokens_count
    sentiment = map(sentiment, -1, 1, 1, 5)
    sentiment = int(sentiment)
    return sentiment
    # if sentiment > 0.2:
    #     return 1
    # elif sentiment < -0.2:
    #     return 0
    # return 1 if (sentiment>0.5) else 0
    # return sentiment


def parse_sentence_LESK(sentence, min_score, max_score, weight, binary=False):
    print ("LESKING INPUTS...")
    token = nltk.word_tokenize(sentence)
    after_tagging = nltk.pos_tag(token)

    sentiment_score = 0.0
    tokens_count = 0
    lemmatizer = WordNetLemmatizer()
    positive_count, negative_count = 0, 0
    pos_score, neg_score = 0, 0
    if sentence == "":
        return None

    for word, tag in after_tagging:
        synset = lesk(token, word)
        if not synset:
            continue
        # print (synset.name())
        swn_synset = swn.senti_synset(synset.name())
        # print(swn_synset)

        sentiment = swn_synset.pos_score() - swn_synset.neg_score()
        if swn_synset.pos_score() > 0:
            pos_score += swn_synset.pos_score()
            positive_count += 1

        if swn_synset.pos_score() > 0:
            neg_score += swn_synset.neg_score()
            negative_count += 1
        
        sentiment = map(sentiment, -1, 1, min_score, max_score)

        sentiment_score += sentiment
        # sentiment = int(sentiment)
        tokens_count += 1
    
    if negative_count == 0:
        negative_count = 1
    if positive_count == 0:
        positive_count = 1

    negative_count = (neg_score/negative_count)*100
    positive_count = (pos_score/positive_count)*100
    
    print ("NEG %: ", negative_count, "POS %:", positive_count, "Weighted NEG %: ", negative_count*weight, "Weighted POS %:", positive_count*weight, weight)
    
    weighted_positive = positive_count * weight
    weighted_negative = negative_count * weight

    # sentiment = (sentiment_score/tokens_count) * weight
    # sentiment = (weighted_positive + weighted_negative) / 2
    sentiment = (weighted_positive - weighted_negative)
    # if not binary:

        # sentiment = map(sentiment, -tokens_count, tokens_count, min_score, max_score)
    # else:
        # sentiment_score = map(sentiment_score, -1, 1, 0, 1)
        # sentiment = (sentiment_score/tokens_count)
        # print (sentiment)
        # sentiment = map(sentiment, -tokens_count, tokens_count, 0, 1)
        # sentiment = map(sentiment, -tokens_count, tokens_count, min_score, max_score)

        # print (sentiment)

    print ("RETUNING SENTIMENT INPUTS...")

    return sentiment
        # if sentiment > 0.2:
        #     return 1
        # elif sentiment < -0.2:
        #     return 0
        # return 1 if (sentiment>0.5) else 0
        # return sentiment


