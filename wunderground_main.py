import html_helper
import re
import datetime

NUM_DAYS = 5

def get_URL(location_param : str, date : 'yyyy-mm-dd') -> 'HTML':
	split = location_param.split('/')
	return 'https://www.wunderground.com/hourly/us/ca/'+split[0]+'/date/'+date+'/'+split[1]+'?cm_ven=localwx_hour'

def get_next_n_days(n : int) -> ['yyyy-mm-dd']:
	result = []
	curr = datetime.date.today()
	for i in range(n):
		curr += datetime.timedelta(days=1)
		result.append('%04d'%(curr.year,) + '-' + '%02d'%(curr.month,) + '-' + '%02d'%(curr.day,))
	return result

def get_filtered_HTML(html : str, pattern : str) -> 'filtered HTML':
	m = re.search(pattern, html)
	return str(m.groups()[0])

def get_table_rows_HTML(html : str) -> ['table rows HTML']:
	return re.findall(r'<tr _ngcontent-c..="">(.*?)</tr>', html)

def get_rainfall_from_tr(html : str) -> float:
	m = re.search(r'([0-9]+.?[0-9]?[0-9]?) in</a>', html)
	return float(m.groups()[0])

def perform_main():
	dates = get_next_n_days(NUM_DAYS)
	params_file = open('location_url_params.txt')
	filter_1 = r'(<table _ngcontent-c..="" id="hourly-forecast-table">.*</table>)'
	filter_2 = r'(<tbody.*</tbody>)'

	for line in params_file:
		for date in dates:
			location_param = line.rstrip('\n')
			total_rainfall = 0
			url = get_URL(location_param, date)
			html = html_helper.get_HTML(url)
			html = get_filtered_HTML(html, filter_1)
			html = get_filtered_HTML(html, filter_2)
			row_htmls = get_table_rows_HTML(html)
			for row in row_htmls:
				total_rainfall += get_rainfall_from_tr(row)
			print(location_param + ' ' + date + ' : ' + str(total_rainfall) + ' in')


if __name__ == '__main__':
	perform_main()