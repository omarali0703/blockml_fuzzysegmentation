from nltk import pos_tag, word_tokenize
from nltk.wsd import lesk
from nltk.parse import stanford, bllip
from nltk.tree import ParentedTree
from nltk.data import find
import os
from spacy.pipeline.dep_parser import DEFAULT_PARSER_MODEL
        

# model_dir = find("models/bllip_wsj_no_aux").path
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'jars/')

def compare_leaves(sentence, leaf_1, leaf_2):
    parent, count = get_lca_dist_list(sentence[0], [leaf_1, leaf_2], 1,1)
    # print(count, parent, leaf_1, get_depth(1, parent, leaf_1), get_depth(1, parent, leaf_2))
    max_depth = max(get_depth(1, parent, leaf_1), get_depth(1, parent, leaf_2))
    # print("MAX", max_depth)
    sim =  1 / max_depth
    return sim


#  Only load this shit once
model_dir = find('models/bllip_wsj_no_aux').path
parser = bllip.BllipParser.from_unified_model_dir(model_dir)   

def generate_parse_tree(input_str, show=True, parse_type='syntax'):
    # STANFORD PARSER
    # parser = stanford.StanfordParser(path_to_jar=filename+'stanford-corenlp-4.2.0-sources.jar', path_to_models_jar=filename+'stanford-corenlp-4.2.0-models.jar')
    # sentences = parser.raw_parse_sents((input_str, ))

    # CHARNIAK
    # print(input_str)
    if parse_type == 'syntax':
        sentences = parser.parse_one(input_str.split())
    elif parse_type == 'dep':
        spacy_dep_tree = None

        config = {
            "moves": None,
            "update_with_oracle_cut_size": 100,
            "learn_tokens": False,
            "min_action_freq": 30,
            "model": DEFAULT_PARSER_MODEL,
        }
        nlp.add_pipe("parser", config=config)
        sentence = to_nltk_tree(spacy_dep_tree)
    else:
        sys.exit("Please specify a valid parsing technique to run Fuzzy Seg")

    sentence_list = []
    for line in sentences:
        for sentence in line:
            # print (type(sentence))
            # sentence = ParentedTree.convert(sentence)
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

def to_nltk_tree(node):
    if node.n_lefts + node.n_rights > 0:
        return Tree(node.orth_, [to_nltk_tree(child) for child in node.children])
    else:
        return node.orth_

def get_lca_dist(root, n1, n2, count1, count2):
    # print(n1, n2)
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
