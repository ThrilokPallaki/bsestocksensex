import csv
import redis as red
import requests
import datetime
import zipfile
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_strdate():
	 date = datetime.date.today() 	
	 if date.weekday() == 6:
		return (date - datetime.timedelta(2)).strftime('%d%m%y') 
 	 elif date.weekday() == 0: 
		return (date - datetime.timedelta(3)).strftime('%d%m%y') 
	 else:
		return (date - datetime.timedelta(1)).strftime('%d%m%y')


def gathering_data():
	base_url = 'http://www.bseindia.com/'
	equity_zip_url = base_url+'/download/BhavCopy/Equity/'
	file_name = 'EQ'+get_strdate()+'_CSV' +'.ZIP'
	try:
		open(os.path.join(BASE_DIR, file_name))
	except:
		req = requests.get(equity_zip_url+file_name)
		with open(os.path.join(BASE_DIR, file_name), 'wb') as zip_file:
			zip_file.write(req.content)


def unzip_file():
	file_name = 'EQ'+get_strdate()+'_CSV' +'.ZIP'
	zip_file = zipfile.ZipFile(os.path.join(BASE_DIR, file_name))
	zip_file.extractall()


def filter_data_push_into_redis():
	file_name = 'EQ'+get_strdate()+'.CSV'
	with open(os.path.join(BASE_DIR, file_name)) as csv_file:
		csv_reader = csv.DictReader(csv_file)
		fieldnames = ['SC_NAME', 'SC_CODE', 'HIGH', 'LOW', 'CLOSE', 'OPEN']
		r = red.Redis()
		r.flushall()
		for dict_row in csv_reader:
			for col in dict_row:
				dict_row[col]=dict_row[col].strip()
			r.hmset(dict_row['SC_NAME'], {key: dict_row[key] for key in fieldnames})
			r.lpush('bse_keys', dict_row['SC_NAME'])
			wlist = dict_row['SC_NAME'].split(' ')
			for w in wlist:
				r.lpush('bse_keys_words',json.dumps(list((w, dict_row['SC_NAME']))))
  


if __name__ == '__main__':
	gathering_data()
	unzip_file()
	filter_data_push_into_redis()














