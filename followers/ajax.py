from dajax.core import Dajax

def assign_num_friends(request):
	dajax = Dajax()
	dajax.assign('#box', 'innerHTML', 'Hello World')
	return dajax.json()