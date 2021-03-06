# anime-get
アニメ情報を取得することができます

# インストール

```bash
$ pip install git+https://github.com/mino-38/anime-get
```

# オプション
-q [検索ワード]
検索ワードに該当するものだけを出力します

例
```bash
$ anime-get -q hogehoge
# >>> hogehogeと名前にある作品のみ取得
```

-Q [年] [季節(数字)]
取得する年を指定します

例
```bash
$ anime-get -Q 2020 1
# >>> 2020年の冬のアニメ情報を取得
```

```
季節一覧  

1: 冬  
2: 春  
3: 夏  
4: 秋  
```

# データの見方

title:  作品名  
title_en:  作品名英語バージョン(無い場合もある)  
title_short1~3:  作品名の略称、最大で3つ  
public_url:  公式サイトのURL  
twitter_account:  ツイッターアカウントid  
twitter_hash_tag:  ツイッターのハッシュタグ  
sex:  男性向けなら0、女性向けなら1  
sequel:  続編作品なら何期目なのかが入る。続編作品でなければ0が入る  
product_companies:  アニメーションを制作した会社名  

(これらのデータは正確ではない場合があります  
また、連続で使用すると使用しているAPIに負荷をかけることになるので注意してください)
