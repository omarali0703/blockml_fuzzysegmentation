from spacy.pipeline.dep_parser import DEFAULT_PARSER_MODEL
import spacy
import os, sys
from nltk import pos_tag, word_tokenize, internals, Tree
from nltk.wsd import lesk
from nltk.parse import stanford, bllip, CoreNLPDependencyParser
from nltk.tree import ParentedTree

from nltk.data import find
internals.config_java(options='-xmx4G')


# model_dir = find("models/bllip_wsj_no_aux").path
dirname = os.path.dirname(__file__)
# Get the parent of  __file__'s dir (fuzzy_segmentation folder)
dirname = os.path.dirname(dirname)
filename = os.path.join(dirname, 'dependencies/jars/')

# get comparison of one leaf


def compare_leaves(sentence, leaf_1, leaf_2):
    parent, count = get_lca_dist_list(sentence[0], [leaf_1, leaf_2], 1, 1)
    # print(count, parent, leaf_1, get_depth(1, parent, leaf_1), get_depth(1, parent, leaf_2))
    max_depth = max(get_depth(1, parent, leaf_1), get_depth(1, parent, leaf_2))

    # print("MAX", max_depth)
    sim = 1 / max_depth
    return sim

# Gets the average for all leaves.


def compare_leaves_AVG(sentence, leaves):
    parent, count = get_lca_dist_list(sentence[0], leaves, 1, 1)
    # print(count, parent, leaf_1, get_depth(1, parent, leaf_1), get_depth(1, parent, leaf_2))
    avg_depth = 0
    # print (type(leaves))
    for leaf in leaves:
        leaf_depth = get_depth(1, parent, leaf)
        avg_depth += leaf_depth

    # print("MAX", max_depth)
    sim = 1 / (avg_depth/len(leaves))
    return sim


#  Only load this shit once
model_dir = find('models/bllip_wsj_no_aux').path

parser = stanford.StanfordParser(path_to_jar=filename+'stanford-corenlp-4.2.0-sources.jar',
                                 path_to_models_jar=filename+'stanford-corenlp-4.2.0-models.jar', java_options='-mx8G', )


def generate_parse_tree(input_str, show=True, parse_type='syntax'):
    print('Generating parse tree....')
    '''
    [ParentedTree('ROOT', [ParentedTree('S', [ParentedTree('NP', [ParentedTree('JJ', ['Cognitive']), ParentedTree('NNS', ['games'])]), ParentedTree('VP', [ParentedTree('VBP', ['involve']), ParentedTree('NP', [ParentedTree('NP', [ParentedTree('DT', ['a']), ParentedTree('NN', ['number'])]), ParentedTree('PP', [ParentedTree('IN', ['of']), ParentedTree('NP', [ParentedTree('NP', [ParentedTree('JJ', ['different']), ParentedTree('NNS', ['games'])]), ParentedTree('VP', [ParentedTree('VBG', ['working']), ParentedTree('NP', [ParentedTree('NP', [ParentedTree('NNS', ['aspects'])]), ParentedTree('PP', [ParentedTree('IN', ['of']), ParentedTree('NP', [ParentedTree('JJ', ['human']), ParentedTree('NN', ['cognition'])])])]), ParentedTree(',', [',']), ParentedTree('PP', [ParentedTree('IN', ['while']), ParentedTree('S', [ParentedTree('VP', [ParentedTree('VBG', ['proposing']), ParentedTree('NP', [ParentedTree('NP', [ParentedTree('DT', ['the']), ParentedTree('NN', ['intersection'])]), ParentedTree('PP', [ParentedTree('IN', ['between']), ParentedTree('NP', [ParentedTree('NP', [ParentedTree('DT', ['the']), ParentedTree('NNS', ['sets'])]), ParentedTree('PP', [ParentedTree('IN', ['of']), ParentedTree('NP', [ParentedTree('NNS', ['concepts']), ParentedTree(',', [',']), ParentedTree('NN', ['fun']), ParentedTree('CC', ['and']), ParentedTree('NN', ['cognition'])])])])])])])])]), ParentedTree(',', [',']), ParentedTree('PP', [ParentedTree('PP', [ParentedTree('IN', ['for']), ParentedTree('NP', [ParentedTree('NP', [ParentedTree('DT', ['the']), ParentedTree('NN', ['improvement'])]), ParentedTree('PP', [ParentedTree('IN', ['of']), ParentedTree('NP', [ParentedTree('NP', [ParentedTree('JJ', ['cognitive']), ParentedTree('NNS', ['functions'])]), ParentedTree(',', ['.']), ParentedTree('S', [ParentedTree('S', [ParentedTree('NP', [ParentedTree('DT', ['The']), ParentedTree('NN', ['attention'])]), ParentedTree('VP', [ParentedTree('VBZ', ['is']), ParentedTree('NP', [ParentedTree('NP', [ParentedTree('DT', ['the']), ParentedTree('JJ', ['main']), ParentedTree('NN', ['point'])]), ParentedTree('VP', [ParentedTree('VBN', ['made']), ParentedTree('PP', [ParentedTree('IN', ['in']), ParentedTree('NP', [ParentedTree('DT', ['this']), ParentedTree('NN', ['study'])])]), ParentedTree(',', [',']), ParentedTree('SBAR', [ParentedTree('IN', ['since']), ParentedTree('S', [ParentedTree('NP', [ParentedTree('PRP', ['it'])]), ParentedTree('VP', [ParentedTree('VP', [ParentedTree('VBZ', ['is']), ParentedTree('ADJP', [ParentedTree('JJ', ['fundamental']), ParentedTree('PP', [ParentedTree('IN', ['to']), ParentedTree('NP', [ParentedTree('DT', ['the']), ParentedTree('NN', ['learning']), ParentedTree('NN', ['process'])])])])]), ParentedTree('CC', ['and']), ParentedTree('VP', [ParentedTree('VB', ['be']), ParentedTree('NP', [ParentedTree('NP', [ParentedTree('VBG', ['recurring']), ParentedTree('NN', ['complaint'])]), ParentedTree('PP', [ParentedTree('IN', ['among']), ParentedTree('NP', [ParentedTree('NNS', ['parents']), ParentedTree('CC', ['and']), ParentedTree('NNS', ['teachers'])])]), ParentedTree('PP', [ParentedTree('IN', ['in']), ParentedTree('NP', [ParentedTree('NNS', ['schools'])])])])])])])])])])])]), ParentedTree('.', ['.']), ParentedTree('S', [ParentedTree('PP', [ParentedTree('IN', ['With']), ParentedTree('NP', [ParentedTree('NP', [ParentedTree('NN', ['respect'])]), ParentedTree('PP', [ParentedTree('IN', ['to']), ParentedTree('NP', [ParentedTree('NP', [ParentedTree('DT', ['the']), ParentedTree('NNS', ['contributions'])]), ParentedTree('PP', [ParentedTree('IN', ['of']), ParentedTree('NP', [ParentedTree('NP', [ParentedTree('JJ', ['digital']), ParentedTree('NNS', ['games'])]), ParentedTree('PP', [ParentedTree('IN', ['to']), ParentedTree('NP', [ParentedTree('NP', [ParentedTree('NN', ['improvement'])]), ParentedTree('PP', [ParentedTree('IN', ['of']), ParentedTree('NP', [ParentedTree('JJ', ['cognitive']), ParentedTree('NNS', ['processes'])])])])])])])])])])]), ParentedTree(',', [',']), ParentedTree('NP', [ParentedTree('NNS', ['researchers'])]), ParentedTree('VP', [ParentedTree('VBP', ['suggest']), ParentedTree('SBAR', [ParentedTree('IN', ['that']), ParentedTree('S', [ParentedTree('NP', [ParentedTree('JJ', ['regular']), ParentedTree('NN', ['practice'])]), ParentedTree('VP', [ParentedTree('VBZ', ['has']), ParentedTree('NP', [ParentedTree('NP', [ParentedTree('DT', ['a']), ParentedTree('JJ', ['significant']), ParentedTree('NN', ['influence'])]), ParentedTree('PP', [ParentedTree('IN', ['on']), ParentedTree('S', [ParentedTree('VP', [ParentedTree('VBG', ['improving']), ParentedTree('NP', [ParentedTree('NP', [ParentedTree('DT', ['the']), ParentedTree('NN', ['performance'])]), ParentedTree('VP', [ParentedTree('VBN', ['related']), ParentedTree('PP', [ParentedTree('IN', ['to']), ParentedTree('NP', [ParentedTree('JJ', ['basic']), ParentedTree('JJ', ['visual']), ParentedTree('NNS', ['skills'])])]), ParentedTree('PRN', [ParentedTree('-LRB-', ['-LRB-']), ParentedTree('NP', [ParentedTree('NP', [ParentedTree('NNP', ['Li']), ParentedTree(',', [',']), ParentedTree('NNP', ['Polat']), ParentedTree(',', [',']), ParentedTree('NNP', ['Scalzo']), ParentedTree(',', [','])]), ParentedTree('CC', ['&']), ParentedTree('NP', [ParentedTree('NNP', ['Bavelier'])])]), ParentedTree(',', [',']), ParentedTree('NP', [ParentedTree('CD', ['2010'])]), ParentedTree('-RRB-', ['-RRB-'])])])])])])])])])])])])])]), ParentedTree(':', [';']), ParentedTree('PP', [ParentedTree('IN', ['on']), ParentedTree('NP', [ParentedTree('DT', ['the']), ParentedTree('NN', ['ability']), ParentedTree('S', [ParentedTree('VP', [ParentedTree('TO', ['to']), ParentedTree('VP', [ParentedTree('VB', ['perceive']), ParentedTree('NP', [ParentedTree('NNS', ['objects'])]), ParentedTree('ADVP', [ParentedTree('RB', ['simultaneously'])])])])]), ParentedTree('PRN', [ParentedTree('-LRB-', ['-LRB-']), ParentedTree('NP', [ParentedTree('NP', [ParentedTree('NNP', ['Dye']), ParentedTree('CC', ['&']), ParentedTree('NNP', ['Bavelier'])]), ParentedTree(',', [',']), ParentedTree('NP', [ParentedTree('CD', ['2010'])])]), ParentedTree(':', [';']), ParentedTree('NP', [ParentedTree('NP', [ParentedTree('NNP', ['Feng']), ParentedTree(',', [',']), ParentedTree('NNP', ['Spence']), ParentedTree(',', [','])]), ParentedTree('CC', ['&']), ParentedTree('NP', [ParentedTree('NNP', ['Pratt'])])]), ParentedTree(',', [',']), ParentedTree('NP', [ParentedTree('CD', ['2007'])]), ParentedTree('-RRB-', ['-RRB-'])])])]), ParentedTree(':', [';'])])])])]), ParentedTree('CC', ['and']), ParentedTree('PP', [ParentedTree('IN', ['on']), ParentedTree('NP', [ParentedTree('DT', ['the']), ParentedTree('NN', ['ability']), ParentedTree('S', [ParentedTree('VP', [ParentedTree('TO', ['to']), ParentedTree('VP', [ParentedTree('VB', ['do']), ParentedTree('NP', [ParentedTree('QP', [ParentedTree('JJR', ['more']), ParentedTree('IN', ['than']), ParentedTree('CD', ['one'])]), ParentedTree('NN', ['task'])]), ParentedTree('PP', [ParentedTree('IN', ['at']), ParentedTree('NP', [ParentedTree('DT', ['the']), ParentedTree('JJ', ['same']), ParentedTree('NN', ['time'])])])])])])])])])])])])]), ParentedTree('PRN', [ParentedTree('-LRB-', ['-LRB-']), ParentedTree('NP', [ParentedTree('NP', [ParentedTree('NNP', ['Boot']), ParentedTree(',', [',']), ParentedTree('NNP', ['Kramer']), ParentedTree(',', [',']), ParentedTree('NNP', ['Simons']), ParentedTree(',', [',']), ParentedTree('NNP', ['Fabiani']), ParentedTree(',', [','])]), ParentedTree('CC', ['&']), ParentedTree('NP', [ParentedTree('NNP', ['Gratton'])])]), ParentedTree(',', [',']), ParentedTree('NP', [ParentedTree('CD', ['2008'])]), ParentedTree('-RRB-', ['-RRB-'])])]), ParentedTree('.', ['.'])])])]
    '''
    # CHARNIAK
    # print(input_str)
    if parse_type == 'syntax':
        # print(input_str)

        # STANFORD PARSER
        print('Running Stanford parser')
        sentences = parser.raw_parse_sents((input_str, ))
        print(sentences)
        print('Finished running Stanford parser')
        # sentences = parser.parse(input_str)
    elif parse_type == 'dep':

        dep_parser = CoreNLPDependencyParser(url='http://localhost:9000')
        print(input_str)
        sentences = list(dep_parser.parse_sents(input_str)).tree()[0]
        # print (sentences[0])
        # nlp.add_pipe("parser", config=config)
        # sentences = [to_nltk_tree(sent.root) for sent in spacy_dep_tree.sents]
    elif parse_type == 'char':
        charn_parser = bllip.BllipParser.from_unified_model_dir(model_dir) #charniak parser

        sentences = charn_parser.parse_one(input_str)
        print(sentences)
    else:
        sys.exit("Please specify a valid parsing technique to run Fuzzy Seg")

    sentence_list = []
    for line in sentences:
        for sentence in line:
            # print (type(sentence))
            # sentence = ParentedTree.convert(sen§tence)
            sentence_list.append(ParentedTree.convert(sentence))
            # print(get_leaf_from_word_index(sentence, 1))
            # print(get_depth(1, sentence[0], sentence[0][1][1][1]))
            # leaf_1 = sentence[0][0][0]
            # leaf_2 = sentence[0][1][1][0][0]
            # print(compare_leaves(sentence, leaf_1, leaf_2))
            # max_height = max(get_depth(2, parent, sentence[0][0][0]), get_depth(2, parent, sentence[0][1][1][0])
            # print(parent)
            # print(count)
            if show:
                for sentence in sentence_list:
                    sentence.draw()
    # return sentence.leaves(), sentence
    return sentence_list


def get_lca_dist(root, n1, n2, count1, count2):
    # print(root, "END ROOT", n1, n2, count1, count2, type(root), type(n1), type(n2), type(count1), type(count2))
    if n2 == None:
        return n1.parent(), max(count1, count2)
    if n1 == None:
        return n2.parent(), max(count1, count2)

    if n1.parent() == n2.parent():
        return n1.parent(), max(count1, count2)
    if get_depth(1, root, n1) < get_depth(1, root, n2):
        return get_lca_dist(root, n1, n2.parent(), count1, count2+1)
    if get_depth(1, root, n1) > get_depth(1, root, n2):
        return get_lca_dist(root, n1.parent(), n2,  count1+1, count2)
    if get_depth(1, root, n1) == get_depth(1, root, n2):
        return get_lca_dist(root, n1.parent(), n2.parent(), count1+1, count2+1)


def get_lca_dist_list(root, leaves, count1, count2):
    # print("HELLO", leaves)
    return get_lca_dist(root, leaves[0], leaves[len(leaves)-1], count1, count2)


def get_depth(depth, root, x):
    if x == root:
        return 0.001
    if x.parent() == root or x.parent() == None:
        return depth
    return get_depth(depth+1, root, x.parent())


def max(i, j):
    if i > j:
        return i
    if j > i:
        return j
    if j == i:
        return j


def get_leaf_from_word_index(tree, index):
    return tree.leaf_treeposition(index)

# output = generate_parse_tree()
