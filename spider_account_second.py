from multiprocessing import Pool
import requests

file = open('account.txt','a+')

channel_list = list(xrange(160000000000,169009999999))

def spider(channel):
	url_info = 'http://教务系统/upload/XXX/{}.jpg'.format(channel)
	info = requests.get(url_info)
	if info.status_code == 404:
		print 'Error...' + str(channel)
		pass
	elif info.status_code ==200:
		print 'Success!!' + str(channel)
		account_info = str(channel) + '\n'
		file.write(account_info)
	else:
		pass
		
if __name__ == '__main__':
	pool = Pool(processes=3)
	pool.map(spider,channel_list)