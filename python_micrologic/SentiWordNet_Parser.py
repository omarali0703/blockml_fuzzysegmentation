from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.corpus import sentiwordnet as swn
from nltk.corpus import wordnet as wn
import nltk
nltk.download('sentiwordnet')
nltk.download('wordnet')
list(swn.senti_synsets('slow'))


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
        synset = synsets[0]
        swn_synset = swn.senti_synset(synset.name())
        print(swn_synset)

        sentiment += swn_synset.pos_score() - swn_synset.neg_score()
        tokens_count += 1
    print(sentiment)
