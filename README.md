# syamu_bot
syamu_gameと会話しよう

## 使い方

```
$ cd engine
$ python bot.py
```

quitで終了します

## 現在の機能
・受け取った単語に対してword2vecによるsyamuの世界観からの文章生成
・syamuを複数体用意してそれぞれに対話させる（強化学習では無いです）
・botの知識は語録から生成、ユーザーから受け取ったことがを知らなかった場合それを学習する
・ブラウザによるGUIでの会話（jqueryによるAjaxを用いています）
