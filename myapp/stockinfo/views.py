from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django_redis import get_redis_connection
from django.shortcuts import render

def index(request):
	sensex_data = []
	error = ''
	con = get_redis_connection('default')
	if request.method=='POST':
		query = request.POST['query'].upper()	
		response_data = con.hgetall(query) if con.exists(query) else ''
		if response_data == '':
			error = 'No data found'
			context = {'error':error}
		else:
			sensex_data.append([query, response_data])
			context = {'sensex_data': sensex_data}
	else:
		for item in con.lrange('bse_keys', -11, -1):
			sensex_data.append([item, con.hgetall(item)])
		sensex_data = [ sensex_data[row] for row in range(len(sensex_data)-1, 0, -1)]
		context = {'sensex_data': sensex_data}
	return render(request, 'stockinfo/index.html', context)

