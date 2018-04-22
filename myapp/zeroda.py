import csv
import redis as red
import requests
import datetime
import zipfile

def get_strdate():
	date = datetime.date.today() 	
	return (date - datetime.timedelta(2)).strftime('%d%m%y') if date.weekday() == 6 else (date - datetime.timedelta(1)).strftime('%d%m%y')


def gathering_data():
	#base_url = 'http://www.bseindia.com/markets/equity/EQReports/BhavCopyDebt.aspx?expandable=3'
	#req = requests.get(base_url)
	#soup = bs(req.content, 'html.parser')
	#iframe = soup.find('iframe')
	#url = iframe.attrs['src']
	#equity_zip_url = base_url.rsplit('/', )[0] + '/'+ url
	#req = requests.get(equity_url)
	#soup = bs(req.content, 'html.parser')
	#links = soup.findAll('a')
	#zip_links = [link['href'] for link in links if 'href' in link.attrs and link['href'].endswith('ZIP')]
	#req = requests.get(zip_links[0])
	base_url = 'http://www.bseindia.com/'
	equity_zip_url = base_url+'/download/BhavCopy/Equity/'
	file_name = 'EQ'+get_strdate()+'_CSV' +'.ZIP'
	try:
		open('/home/thrilok/'+file_name)
	except:
		req = requests.get(equity_zip_url+file_name)
		with open('/home/thrilok/'+file_name, 'wb') as zip_file:
			zip_file.write(req.content)


def unzip_file():
	file_name = 'EQ'+get_strdate()+'_CSV' +'.ZIP'
	zip_file = zipfile.ZipFile('/home/thrilok/'+file_name)
	zip_file.extractall()


def filter_data_push_into_redis(): 
	str_date = datetime.date.today().strftime('%d%m%y')
	file_name = 'EQ'+get_strdate()+'.CSV'
	with open('/home/thrilok/'+file_name) as csv_file:
		csv_reader = csv.DictReader(csv_file)
		fieldnames = ['SC_NAME', 'SC_CODE', 'HIGH', 'LOW', 'CLOSE', 'OPEN']
		#exclude_fieldnames = ['PREVCLOSE', 'LAST', 'NO_OF_SHRS', 'NET_TURNOV', 'NO_TRADES', 'SC_GROUP', 'TDCLOINDI', 'SC_TYPE']
		r = red.Redis()
		for dict_row in csv_reader:
			for col in dict_row:
				dict_row[col]=dict_row[col].strip()
			r.hmset(dict_row['SC_NAME'], {key: dict_row[key] for key in fieldnames[1:]})
			r.lpush('bse_keys', dict_row['SC_NAME'])
  

#def push_into_redis():
#	with open('/home/thrilok/new.csv', 'r') as csv_file:
#		csv_reader = csv.DictReader(csv_file, delimiter='\t')
#	 	r = red.Redis()
#		for row in csv_reader:
#			a = {key: row[key] for key in row.keys() if key != 'SC_NAME'}
#			r.hmset(row['SC_NAME'], a)
#


if __name__ == '__main__':
	gathering_data()
	unzip_file()
	filter_data_push_into_redis()














