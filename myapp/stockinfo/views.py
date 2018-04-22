
from django_redis import get_redis_connection
from django.shortcuts import render
import pdb
# Create your views here.

def index(request):
	sensex_data = []
	con = get_redis_connection('default')
	if request.method=='POST':
		query_data = con.hgetall(request.POST['query'])
		sensex_data.append([request.POST['query'], query_data])
		context = {'sensex_data': sensex_data}
	else:
		for item in con.lrange('bse_keys', -11, -1):
			sensex_data.append([item, con.hgetall(item)])
		sensex_data = [ sensex_data[row] for row in range(len(sensex_data)-1, 0, -1)]
		context = {'sensex_data': sensex_data}
	return render(request, 'stockinfo/index.html', context)

def search(request, query):
	con = get_redis_connection('default')
	data = con.hgetall(query)
	return render(request, 'stockinfo/index.html', {'data':data})
