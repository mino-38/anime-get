#!/usr/bin/env python3

import requests
import sys
import os
import time
import datetime as dt

class AnimeGetError(Exception):
    pass

class Anime_Get:
    api_url = 'https://api.moemoe.tokyo/anime/v1/master'
    arg = sys.argv

    def GetAnimeInformation(self) -> requests.models.Response.json:
        if '-h' in self.arg or '--help' in self.arg:
            print('基本的な記述\nanime-get <オプション>\n\n<オプション一覧>\n-q\n作品名で検索することができます\n検索キーワードは略称でも大丈夫です\n複数の検索キーワードを使用する場合は、\'&\'で区切ってください\n使用例:  anime-get -q A&B&C\n(※空白を開けないでください。空白を開けると正しく動作しない場合があります)\n\n-Q\n指定された季節や年のアニメ一覧を表示します\n季節の指定は以下の通りです\n1 冬季\n2 春季\n3 夏季\n4 秋季\nまた、-qオプションとの併用もできます\n使用例:  anime-get -q A -Q 2020 1\n\n[データの見方]\ntitle  作品名\ntitle_en  作品名英語ver(無い場合もある)\ntitle_short1~3  作品名の略称、最大で3つ\npublic_url  公式サイトのURL\ntwitter_account  ツイッターアカウントid\ntwitter_hash_tag  ツイッターのハッシュタグ\nsex  男性向けなら0、女性向けなら1\nsequel  続編作品なら何期目なのかが入る。続編作品でなければ0が入る\nproduct_companies  アニメーションを制作した会社名\n\n(これらのデータは正確ではない場合があります\nまた、出力後に処理が少し停止するのはDos/DDos攻撃対策です\n予めご了承ください)')
            sys.exit()
        elif not '-Q' in self.arg:
            date = dt.datetime.now()
            self.year = str(date.year)
            month = int(date.month)
            self.n = self.seasons(month)[0]
        else:
            try:
                self.year = int(self.arg[self.arg.index('-Q')+1])
                self.n = int(self.arg[self.arg.index('-Q')+2])
            except ValueError:
                raise AnimeGetError('Please enter an integer')
                sys.exit()
        self.season = self.season_check(self.n)
        self.result = self.request()

    def request(self, date=dt.datetime.now()) -> requests.models.Response.json:
        while True:
            url = '{0}/{1}/{2}'.format(self.api_url, self.year, self.n)
            r = requests.get(url)
            if 400 <= r.status_code <= 499 or (result := r.json()) == []:
                try:
                    date -= dt.timedelta(days=1)
                    self.year = date.year
                    if self.n != 1:
                        self.n -= 1
                    else:
                        self.n = 4
                    self.season = self.season_check(self.n)
                    continue
                except:
                    raise AnimeGetError('Incorrect seasonal or year designation')
                    sys.exit()
            elif r.status_code != 200:
                raise AnimeGetError('Unexpected error')
                sys.exit()
            else:
                break
        return result

    def season_check(self, n) -> str:
        if n == 1:
            return '冬季'
        elif n == 2:
            return '春季'
        elif n == 3:
            return '夏季'
        elif n == 4:
            return '秋季'

    def seasons(self, month):
        if type(month) is not int:
            raise AnimeGetError('please give an integer as an argument')
        if 1 <= month <= 3:
            n = 1
        elif 4 <= month <= 6:
            n = 2
        elif 7 <= month <= 9:
            n = 3
        elif 10 <= month <= 12:
            n = 4
        else:
            raise AnimeGetError('please give an integer from 1 to 12 as an argument')
        return (n, self.season_check(n))

    def stdout(self) -> None:
        if not '-q' in self.arg:
            for d in self.result:
                for key, item in d.items():
                    if key == 'id':
                        print()
                        continue
                    elif key == 'cours_id' or key == 'created_at' or key == 'updated_at' or key == 'city_code' or item == '':
                        continue
                    else:
                        print('{}:  {}'.format(key, item))
            print("\n{0}年{1}のアニメ数の合計は、 '{2}' です".format(self.year, self.season, len(self.result)))
        else:
            search_word = self.arg[self.arg.index('-q')+1].split('&')
            result = []
            [_ for _ in [a for a in self.result for s in search_word if s in a['title'] or s in a['title_short1'] or s in a['title_short2'] or s in a['title_short3']] if not _ in result and result.append(_)]
            for d in result:
                for key, item in d.items():
                    if key == 'id':
                        print()
                        continue
                    if key == 'cours_id' or key == 'created_at' or key == 'updated_at' or key == 'city_code' or item == '':
                        continue
                    print('{}:  {}'.format(key, item))
            print('\n{}件ヒットしました'.format(len(result)))

def main() -> None:
    anime = Anime_Get()
    anime.GetAnimeInformation()
    anime.stdout()

if __name__ == '__main__':
    main()