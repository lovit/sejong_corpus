def toshort(tag):
    if tag[0] == 'N': return 'Noun'
    if tag[:2] == 'VV': return 'Verb'
    if tag[:2] == 'VX': return 'Verb'        # 보조용언: 않/VX+았/EP+다/EF+./SF
    if tag[:2] == 'VA': return 'Adjective'
    if tag[:2] == 'MA': return 'Adverb'
    if tag[0] == 'E': return 'Eomi'
    if tag[0] == 'J': return 'Josa'
    if tag[:2] == 'IC': return 'Exclamation' # 감탄사
    if tag[:2] == 'MM': return 'Determiner'  # 관형사
    if tag[:3] == 'XPN': return 'Noun'       # 체언접두사
    if tag[:2] == 'VC' or tag[:2] == 'XS': return tag
    if tag[:2] == 'SN': return 'SN'
    if tag[0] == 'S': return 'Symbol'
    if tag == 'XR': return 'Noun'
    if tag == 'Noun': return tag
    if tag == 'Adjective': return tag
    if tag == 'Adverb': return tag
    if tag == 'Verb': return tag 
    if tag == 'Determiner': return tag
    if tag == 'Eomi': return tag
    if tag == 'Josa': return tag
    if tag == 'Exclamation': return tag
    return None

def Nouns(pos):
    (b,e) = (-1, -1)
    for i, (word, tag) in enumerate(pos):
        if b < 0 and (tag[0] == 'N' or tag == 'SN' or tag == 'NR' or tag == 'XR'):
            (b, e) = (i, i)
            continue
        if b >= 0 and not (tag[0] == 'N' or tag == 'XSN' or tag == 'SN'):
            e = i
            break
    if pos[-1][1][0] == 'N' or pos[-1][1] == 'SN' or pos[-1][1] == 'XSN' or pos[-1][1] =='NR':
        e = len(pos)
    if b >= 0 and e > b:
        pos = pos[:b] + [(''.join((w for w,_ in pos[b:e])), 'Noun')]+ pos[e:]
    return pos

def PostfixNouns(pos):
    (b,e) = (-1, -1)
    for i, (word, tag) in enumerate(pos):
        if b < 0 and (tag == 'MM' or tag == 'XPN' or tag == 'XR'):
            (b, e) = (i, i)
            continue
        if b >= 0 and not (tag[0] == 'N' or tag == 'SN' or tag == 'MM' or tag == 'XPN' or tag == 'NR'):
            e = i
            break
    if pos[-1][1][0] == 'N' or pos[-1][1] == 'SN':
        e = len(pos)
    if b >= 0 and e > b:
        pos = pos[:b] + [(''.join((w for w,_ in pos[b:e])), 'Noun')]+ pos[e:]
    return pos

def Nountize(pos):
    idx = [i for i, (_, tag) in enumerate(pos) if (tag == 'XSN' or tag == 'ETN')]
    if not idx:
        return pos
    e = max(idx)+1
    return [(''.join((w for w,_ in pos[:e])), 'Noun')] + pos[e:]

def VVAtize(pos):
    idx = [i for i, (_, tag) in enumerate(pos) if tag == 'VCP' or tag == 'XSA' or tag == 'XSV']
    if not idx:
        return pos
    (b,e) = (-1, max(idx)+1)
    for i, (word, tag) in enumerate(pos):
#         if b < 0 and (tag[0] == 'N' or tag == 'SN' or tag == 'XR' or tag == 'MAG' or tag[0] == 'V'):
        if b < 0 and (tag == 'XR' or tag == 'MAG' or tag[0] == 'V' or tag == 'XSA' or tag == 'XSV'):
            b = i
            break
    if b == -1: b = e-1
    if b > e: b = 0
    if b >= 0 and e >= b:
        tag = 'Verb' if pos[e-1][1] == 'XSV' else 'Adjective'
        pos = pos[:b] + [(''.join((w for w,_ in pos[b:e])), tag)]+ pos[e:]
    return pos

def negation(pos):
    idx = [i for i, (_, tag) in enumerate(pos) if tag == 'VCN']
    if not idx:
        return pos
    e = max(idx) + 1
    b = [i for i, (_, tag) in enumerate(pos) if (tag[0] == 'V')]
    if not b: b = max(0, e-1)
    else: b = min(b)
    pos = pos[:b] + [(''.join((w for w,_ in pos[b:e])), 'Verb')]+ pos[e:]
    return pos

def negative_verb(pos):
    if not [tag for word, tag in pos if (word == '안' or word == '못') or tag == 'MAG']:
        return pos
    (b, e) = (-1, -1)
    for i, (word, tag) in enumerate(pos):
        if b < 0 and ((word == '안' or word == '못') and tag == 'MAG'):
            (b, e) = (i, i)
            continue
        if b >= 0 and not (tag[0] == 'V'):
            e = i
            break
    if pos[-1][1][0] == 'V':
        e = len(pos)
    if b >= 0 and e > b:
        pos = pos[:b] + [(''.join((w for w,_ in pos[b:e])), pos[e-1][1])]+ pos[e:]
    return pos

def Eomi(pos):
    b = -1
    for i, (word, tag) in enumerate(pos):
        if tag[0] == 'E':
            b = i
            break
    if b >= 0:
        return pos[:b] + [(''.join((w for w,_ in pos[b:])), 'Eomi')]
    return pos

def Josa(pos):
    b = -1
    for i, (word, tag) in enumerate(pos):
        if tag[0] == 'J':
            b = i
            break
    if b >= 0:
        return pos[:b] + [(''.join((w for w,_ in pos[b:])), 'Josa')]
    return pos

def detach_symbol(pos, remove_symbol=True):
    pos_ = []
    symbol_idx = [i for i, (_, tag) in enumerate(pos) if tag[0] == 'S' and not (tag == 'SN')]
    if not symbol_idx:
        return _process(pos)
    if not remove_symbol and symbol_idx[0] == 0:
        pos_ += [pos[0]]
    for b, e in zip([-1] + symbol_idx, symbol_idx + [len(pos)]):
        b += 1
        if b == e: continue
        pos_ += _process(pos[b:e])
        if not remove_symbol and e < len(pos):
            pos_ += [pos[e]]
    return pos_

def _process(pos):
    pos = Nouns(pos)
    pos = PostfixNouns(pos)
    pos = Nountize(pos)
    pos = VVAtize(pos)
    pos = negation(pos)
    pos = negative_verb(pos)
    pos = Eomi(pos)
    pos = Josa(pos)
    return pos

def hardrule(pos):
    def rule(p):
        if p[0] == '하아서이' and p[1] == 'Adjective': return ('해서', 'Adjective')
        return p
    return [rule(p) for p in pos]

def process(pos):
    pos = detach_symbol(pos)
    pos = [(w,toshort(t)) for w,t in pos]
    pos = [p for p in pos if not (p[1] == None)]
    pos = Nouns(pos)
    pos = hardrule(pos)
    return pos