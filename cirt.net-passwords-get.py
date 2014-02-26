from bs4 import BeautifulSoup as beautifulsoup
from urllib import request, parse
from time import sleep, time, ctime
import re, threading, datetime

url = 'http://cirt.net/passwords'
cs_url = 'http://cirt.net/passwords?vendor='
patt_href = '://'#去除包含相关文档的连接
threads = []
changshang = []


def huoqu(huoqu_url):#打开一个厂商默认用户密码的页面
	url_hq = cs_url+parse.quote(huoqu_url)#得到具体页面url,需要quote编码，不然会出错
	print(url_hq)
	requ = request.urlopen(url_hq)
	response = requ.read()
	response_decode = response.decode()
	bs_huoqu = beautifulsoup(response_decode)
	print('\n厂商名称：{}'.format(huoqu_url))	
	f_w.write('厂商名称：{}'.format(huoqu_url) + '\n')
	lock = threading.Lock()#加入线程锁，防止争抢资源，一个一个的输出不会乱
	lock.acquire()	

	for c in bs_huoqu.find_all('tr'):
		result = re.search(patt_href, c.get_text())
		if result is not None:
			pass
		else:
			result_title = re.match('\d+', c.get_text())#标题直接输出，不用像下面那样分割
			flag = False
			if result_title is  None:#不知道啥原因，只能有一行语句，无奈只好返回标志
				flag = True
			else:
				print(c.get_text())
				f_w.write(c.get_text() + '\n')
			if flag:#用于输出格式好看点， username : password 
				d = c.get_text('\t: ')
				split_v = d.split(':')
				v1 = split_v[0]#User ID 或者PASSWORD
				v1 = v1.strip('\t')
				length = len(v1)
				if length == 8:
					print(c.get_text(' : '))
					f_w.write(c.get_text(' : ') + '\n')
				else:
					print(c.get_text('\t : '))
					f_w.write(c.get_text('\t : ') + '\n')
	print('\n\n')
	f_w.write('\n')#每个厂商之间隔一行
	lock.release()

def main():
	global f_w
	t = datetime.datetime.now()
	t_format = t.strftime('%Y-%m-%d-%H-%M-%S')#输出时间格式
	f_name = 'cirt.net-passwords-' + t_format + '.txt'
	f_w = open(f_name, 'w+')

	req = request.urlopen(url)	 
	resp = req.read()
	resp_decode = resp.decode()
	#print(resp_decode)
	bs = beautifulsoup(resp_decode)
	print('\n starting to process...\n')
	for a in bs.find_all('tr'):#这个是用于处理页面厂商名称的，用于下面获取厂商页面的默认密码
	#print(a)  #格式为  <tr><td><a href="?vendor=Huawei Technologies Co">Huawei Technologies Co</a></td><td><a href="?vendor=Hyperic, Inc.">Hyperic, Inc.</a></td><td><a href="?vendor=IBM">IBM</a></td></tr>
		for b in a.find_all('a'):
		#print('\n')
			#print(b.get_text())#打印出厂商名称 Huawei Technologies Co
			cs_name = b.get_text()
			changshang.append(cs_name)
	
	print(changshang)
	length_cs = len(changshang)
	print('cs len is :{}'.format(length_cs))
	for i in range(0, length_cs, 10):#使用多线程  
		k = length_cs -i 
		if k>10:
			k = 10
		else:
			k = k
		for j in range(k):#使用多少(k)个线程, 输出时需要价格锁Lock，濡染会很乱
			j = i+j
			t = threading.Thread(target = huoqu, args = (changshang[j],))
			threads.append(t)
		for m in range(len(threads)):
			threads[m].start()
		for n in range(len(threads)):
			threads[n].join()
		threads.clear()
	print('工作完成，我要睡一会了...')
	sleep(6)
	f_w.close()

if __name__ == '__main__':
	t1 = time()
	print('start at : {}'.format(ctime()))
	main()
	t2 = time()
	print('stop at : {}'.format(ctime()))
	print('time elasped : {0:.2f} s'.format(t2-t1))
