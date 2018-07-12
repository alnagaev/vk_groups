import requests
import time
import pandas as pd
from collections import defaultdict

token = open('token.txt', 'r').read()


class ActiveUsers:
    def __init__(self, gid):
        self.gid = gid

    def postParser(self):
        r = requests.post('https://api.vk.com/method/execute.postsGet?id='+
                          str(self.gid)+'&offset='+str(0)+'&v='+'5.73'+'&count='+
                          str(100)+'&access_token='+token).json()['response']

        count = r[0]
        ids = r[1]
        return (count, ids)


    # post_ids = postParser(self.gid)[1]
    def all_users(self):
        r = requests.post('https://api.vk.com/method/execute.groupMembers?group_id='+
                          str(self.gid)+'&offset='+str(0)+'&v='+'5.73'+'&count='+str(5000)
                          +'&access_token='+token).json()['response']
        s = defaultdict(list)
        ##################################################################################
        members_count = r[0] #количество участников
        for k,v in r[1][0].items():
            s[k].extend(v)

        if members_count>5000:
            for offset in range(5000, members_count, 5000):
                try:
                    count = offset + 5000
                    r = requests.post('https://api.vk.com/method/execute.groupMembers?group_id='+
                                     str(self.gid)+'&offset='+str(offset)+
                                     '&v='+'5.73'+'&count='+
                                     str(count)+'&access_token='+token).json()['response'][1][0]
                    for k,v in r.items():
                        s[k].extend(v)
                except Exception:
                    pass

        result = pd.DataFrame.from_dict(s)
        result['bdate'] = pd.to_datetime(result['bdate'], errors = 'coerce',
                                            yearfirst = True)
        result['bdate'] = result['bdate'].dt.year
        try:
            result.to_csv('all_users/{}.csv'.format(self.gid))
            print('Файл {} записан'.format(self.gid))
        except Exception as e:
            print(str(e)+' запись файла {} не удалась'.format(self.gid))

    @property
    def LikersParser(self):
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
        result['bdate'] = pd.to_datetime(result['bdate'], errors = 'coerce',
                                            yearfirst = True)
        result['bdate'] = result['bdate'].dt.year
        try:
            result.to_csv('posts/{}.csv'.format(self.gid))
            print('Файл {} записан'.format(self.gid))
        except Exception as e:
            print(str(e)+' запись файла {} не удалась'.format(self.gid))

    @property
    def RepostersPaser(self):
        self.ids = self.postParser()[1]
        s = defaultdict(list)
        for i in self.ids:
            try:
                r = requests.post('https://api.vk.com/method/execute.reposters?id='+
                          str(self.gid)+'&number='+str(i)+'&v='+'5.73'+
                          '&access_token='+token).json()['response'][0]
                for k,v in r.items():
                    s[k].extend(v)

            except Exception as e:
                pass
        result = pd.DataFrame.from_dict(s)
        result['bdate'] = pd.to_datetime(result['bdate'], errors = 'coerce', yearfirst = True)
        result['bdate'] = result['bdate'].dt.year
        try:
            result.to_csv('posts/{}.csv'.format(self.gid))
            print('Файл {} записан'.format(self.gid))
        except Exception as e:
            print(str(e)+' запись файла {} не удалась'.format(self.gid))



def main():
    case = ActiveUsers(75617836).all_users()


if __name__ == '__main__':
    main()
