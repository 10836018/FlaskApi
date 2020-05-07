from flask import Flask, request, jsonify

import json
import jieba

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def postJson():
    if request.method == 'POST':
        data = json.loads(request.get_data().decode('utf-8'))
        print("get POST request data: ", data)

        answer = data["answer"]

        # -----------------------
        # 刪除文檔中的標點符號
        # -----------------------
        cleanText = "".join(c for c in answer if c not in ('；', '，', '。', '！', '：', '「', '」', '…', '、', '？', '【', '】',
        '.', ':', '?', ';', '!', '~', '`', '+', '-', '<','>', '/', '[', ']', '{', '}', "'", '"'))

        # -----------------------
        # 進行分詞
        # -----------------------
        words = jieba.cut(cleanText, cut_all=False)

        # -----------------------
        # 讀入停用詞
        # -----------------------
        stopwords = {}.fromkeys([line.rstrip() for line in open('stopWords.txt', encoding='utf8')])

        # -----------------------
        # 將分詞詞頻加入hash中
        # -----------------------
        myHash = {};
        for word in words:
            if word not in stopwords:
                if word in myHash:
                    myHash[word] += 1
                else:
                    myHash[word] = 1

        items = [(v, k) for k, v in myHash.items()]
        items.sort()
        items.reverse()
        items = [(k, v) for v, k in items]

        ans = {
                'answer': items
        }

        '''for (wrd, cnt) in items:
            ans = {
                'answer': wrd,
                'cnt': cnt
            }'''

        return ans

    elif request.method == 'GET':
        return 'ok!'

    #POST的到http://127.0.0.1:5000/
    #--host=0.0.0.0--port=5000
    if __name__ == "__main__":
        app.debug = True
        app.run()

