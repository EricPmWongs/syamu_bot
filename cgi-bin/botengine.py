from gensim.models import word2vec
from janome.tokenizer import Tokenizer
import os, re, json, random

model_file = "syamu_w2v_model.model"
dict_file = "syamu_markov.json"
dic = {}
tokenizer = Tokenizer() # janome

# 辞書に単語を記録する --- (*1)
def register_dic(words):
    global dic
    if len(words) == 0: return
    tmp = ["@"]
    for i in words:
        word = i.surface
        if word == "" or word == "\r\n" or word == "\n": continue
        tmp.append(word)
        if len(tmp) < 3: continue
        if len(tmp) > 3: tmp = tmp[1:]
        set_word3(dic, tmp)
        if word == "。" or word == "？":
            tmp = ["@"]
            continue
    # 辞書を更新するごとにファイルへ保存
    json.dump(dic, open(dict_file,"w", encoding="utf-8"))

# 三要素のリストを辞書として登録
def set_word3(dic, s3):
    w1, w2, w3 = s3
    if not w1 in dic: dic[w1] = {}
    if not w2 in dic[w1]: dic[w1][w2] = {}
    if not w3 in dic[w1][w2]: dic[w1][w2][w3] = 0
    dic[w1][w2][w3] += 1

# 作文する --- (*2)
def make_sentence(head):
    if not head in dic: return ""
    ret = []
    if head != "@":
        ret.append(head)
    top = dic[head]
    w1 = word_choice(top)
    w2 = word_choice(top[w1])
    ret.append(w1)
    ret.append(w2)
    while True:
        if w1 in dic and w2 in dic[w1]:
            w3 = word_choice(dic[w1][w2])
        else:
            w3 = ""
        ret.append(w3)
        if len(ret) >= 10:
            ret.append('。')
            break

        if w3 == "。" or w3 == "？" or w3 == "": break
        w1, w2 = w2, w3
    return "".join(ret)

#単語をランダムに抽出
def word_choice(sel):
    keys = sel.keys()
    return random.choice(list(keys))

#word2vecで似た単語を検出
def w2v(word):
    like_words = model.most_similar(positive=[word])
    return like_words[0][0]

# チャットボットに返答させる --- (*3)
def make_reply(text):
    # まず単語を学習する
    if text[-1] != "。": text += "。"
    words = tokenizer.tokenize(text)
    register_dic(words)
    # 辞書に単語があれば、そこから話す
    for w in words:
        face = w.surface
        ps = w.part_of_speech.split(',')[0]
        if ps == "感動詞":
            return face + "。"
        if ps == "名詞" or ps == "形容詞":
            wface = w2v(face)
            if wface in dic:
                return make_sentence(wface)
            elif face in dic:
                return make_sentence(face)
    return make_sentence("@")

# 辞書があれば最初に読み込む
dic = json.load(open('./src/' + dict_file,"r"))
model = word2vec.Word2Vec.load('./src/' + model_file)