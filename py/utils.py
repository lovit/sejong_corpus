def load(fname, encoding='utf-16le'):
    with open(fname, encoding=encoding) as f:
        docs = [doc.strip() for doc in f]
    return docs

def load_processed_corpus(fname, encoding='utf-8'):
    with open(fname, encoding=encoding) as f:
        docs = [doc.strip().split('\t') for doc in f]
    return tuple(zip(*docs))

def tageojeol_to_tuple(e):
    if '++' in e:
        return ((),())
    tp = [w.split('/') for w in e.split('+') if not '//' in w]
    return tuple(zip(*tp))

def get_sentences(fname):
    def replace(doc):
        if '</s>' in doc: return '</p>'
        if '<s n' in doc: return '<p>'
        return doc.strip()
    def sentence_to_tokens(sentence):
        sentence = sentence.replace(' + ', '+')
        tokens = sentence.split('\n')
        tokens = [tuple(t.split('\t')[1:]) for t in tokens if len(t.split('\t')) == 3]
        return tokens

    with open(fname, encoding='utf-16le') as f:
        docs = [replace(doc) for doc in f]
    docs = '\n'.join(docs)
    sentences = docs.split('</p>')
    sentences = [s.split('<p>')[-1] for s in sentences]
    sentences = [sentence_to_tokens(s) for s in sentences]
    sentences = [s for s in sentences if s]
    return sentences