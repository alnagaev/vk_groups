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
        result['bdate'] = pd.to_datetime(result['bdate'], errors = 'coerce', yearfirst = True)
        result['bdate'] = result['bdate'].dt.year
		return result
        try:
            writer = result.to_csv('likers/{}.csv'.format(self.gid))
            print('Файл записан')
        except Exception as e:
            print(str(e))

	
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
		return result 
		
		
	def write_csv(self):
		if __name__ == self.RepostersPaser:
			try:
				writer = self.RepostersPaser.to_csv('reposters/{}.csv'.format(self.gid))
				print('Файл записан')
			except Exception as e:
				print(str(e))
		if __name__ == self.LikersParser:
			try:
				writer = self.LikersParser.to_csv('likers/{}.csv'.format(self.gid))
				print('Файл записан')
			except Exception as e:
				print(str(e))			


def main():
    case = ActiveUsers(-75617836).RepostersPaser()


if __name__ == '__main__':
    main()
