from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django_redis import get_redis_connection
from django.shortcuts import render
import json

def index(request):
	sensex_data = []
	error = ''
	page = request.GET.get('page')
	con = get_redis_connection('default')
	bse_keys = con.lrange('bse_keys', 0, con.llen('bse_keys'))
	if request.method=='POST':
		query = request.POST['query'].upper()
		keycandidates = (w1 for w1 in bse_keys if query in w1)	
		sensex_data = [[con.hgetall(k)] for k in keycandidates]
		context = {'sensex_data': sensex_data}
		if sensex_data == None or sensex_data == []:
			error = 'No data found'
			context = {'error':error}
	else:
		for item in bse_keys:
			sensex_data.append([con.hgetall(item)])
		sensex_data = [ sensex_data[row] for row in range(len(sensex_data)-1, 0, -1)]	
		try:		
			paginator = Paginator(sensex_data, 10)
			sensex_data = paginator.page(page)
		except PageNotAnInteger:
			sensex_data = paginator.page(1)
		except EmptyPage:
			sensex_data = paginator.page(paginator.num_pages)
		context = {'sensex_data': sensex_data}
	return render(request, 'stockinfo/index.html', context)



