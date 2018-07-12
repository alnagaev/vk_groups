import requests
import datetime
import pandas as pd
from collections import defaultdict


token = open('token.txt', 'r').read()
ids = pd.read_excel('groups_Ivan.xlsx')['Id'].tolist()
ids_ = ['-'+str(x) for x in ids]

class PostParser:
    def __init__(self, owner_id):
        self.owner_id = owner_id

    @property
    def get_members_list_id(self):
        # creating defaultdict
        s = defaultdict(list)
        #запрашиваем данные о постах
        r = requests.post('https://api.vk.com/method/execute.wallGet?id='+
                          str(self.owner_id)+'&offset='+str(0)+'&v='+'5.73'+
                          '&access_token='+token).json()['response']

        for i in range(len(r)):
            for k, v in r[i].items():
                s[k].extend(v)

        date = []
        for i in s['dates']:
            date.append(datetime.datetime.fromtimestamp(i).strftime('%Y-%m-%d'))

        s['dates'] = date
        df = pd.DataFrame.from_dict(s)
        df['gid'] = self.owner_id
        return df

    def write_excel(self):
        #Функция для записи датафрейма в эксель
        try:
            writer = pd.ExcelWriter('posts/{}.xlsx'.format(self.owner_id))
            self.get_members_list_id.to_excel(writer,'Sheet1')
            writer.save()
            print('Файл {} записан'.format(self.owner_id))
        except Exception as e:
            print(str(e)+' запись файла {} не удалась'.format(self.owner_id))


    def write_csv(self):
        #Запись датафрейсма в csv формат
        try:
            writer = self.get_members_list_id.to_csv('posts/{}.csv'.format(self.owner_id))
            print('Файл {} записан'.format(self.owner_id))
        except Exception as e:
            print(str(e)+' запись файла {} не удалась'.format(self.owner_id))

def main():
    PostParser().write_excel()


if __name__ == '__main__':
    main()
