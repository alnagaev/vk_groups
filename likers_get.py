import requests
import time
import pandas as pd
from collections import defaultdict

token = open('token.txt', 'r').read()


class LikeParser:
    def __init__(self, gid):
        self.gid = gid
        self.usersParse()

    def postParser(self):
        r = requests.post('https://api.vk.com/method/execute.postsGet?id='+
                          str(self.gid)+'&offset='+str(0)+'&v='+'5.73'+'&count='+
                          str(100)+'&access_token='+token).json()['response']

        count = r[0]
        ids = r[1]
        return (count, ids)


    def usersParse(self):
        self.ids = self.postParser()[1]
        s = defaultdict(list)
        for i in self.ids:
            try:
                r = requests.post('https://api.vk.com/method/execute.likesP?id='+
                          str(self.gid)+'&number='+str(i)+'&v='+'5.73'+
                          '&access_token='+token).json()['response'][0]
                for k,v in r.items():
                    s[k].extend(v)

            except Exception as e:
                pass

        result = pd.DataFrame.from_dict(s)
        try:
            writer = pd.ExcelWriter('likers/{}.xlsx'.format(self.gid))
            result.to_excel(writer,'Sheet1')
            writer.save()
            print('Файл записан')
        except Exception as e:
            print(str(e))


def main():
    case = LikeParser(-1).usersParse()


if __name__ == '__main__':
    main()
