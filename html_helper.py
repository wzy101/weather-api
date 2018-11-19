import urllib.parse
import urllib.request

DATA = urllib.parse.urlencode({'s':'basic', 'submit': 'search'}).encode('utf-8')

def get_HTML(url : str) -> 'HTML':
	req = urllib.request.Request(url, DATA)
	resp = urllib.request.urlopen(req)
	return str(resp.read())