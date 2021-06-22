#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Dependancies
import json,html,re,time
from bs4 import BeautifulSoup
from datetime import datetime

import requests
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


import sqlite3

r = requests.Session()
retries = Retry(total=5,
                backoff_factor=2,
                status_forcelist=[ 500, 502, 503, 504 ])
r.mount('http://', HTTPAdapter(max_retries=retries))

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'}
headersjson = {'accept':'application/json','accept-encoding':'gzip, deflate','user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}


class moneda():

	

	def get_html(self,url):
		try:
			result_html = r.get(url, headers=headersjson, timeout=20, allow_redirects=True)
		except Exception as e:
			print('Error: %s' % e)
			self.countdown(0,3,'Se reintentara en:')
			result_html = r.get(url, headers=headersjson, timeout=20, allow_redirects=True)
		src_html = result_html.content
		soup_html = BeautifulSoup(src_html, 'html.parser')
		return soup_html

	def countdown(self,p,q,texto = ''):
	    i=p
	    j=q
	    k=0
	    while True:
	        if(j==-1):
	            j=59
	            i -=1
	        if(j > 9):  
	            print(texto +' '+str(k)+str(i)+":"+str(j), end="\r")
	        else:
	            print(texto +' '+str(k)+str(i)+":"+str(k)+str(j), end="\r")
	        time.sleep(1)
	        j -= 1
	        if(i==0 and j==-1):
	            break
	    if(i==0 and j==-1):
	        print(texto +' 00:00\n', end="\r")


	def inser_data_to_db(self, name, valor, key):

		conn = sqlite3.connect('test.db')

		conn.execute('''CREATE TABLE IF NOT EXISTS `change_rate`
		         (id INT PRIMARY KEY NOT NULL,
		         NAME           TEXT    NOT NULL,
		         VALOR          REAL,
		         date_time     TEXT);''')

		update = False
		try:
			select = "SELECT * from `change_rate` where NAME = '" + name + "'"
			# print(select)
			data = conn.execute(select)
			if data.fetchall():
				update = True
		except Exception as e:
			print(e)

		fecha_hora = datetime.now()

		print(fecha_hora)

		if update:
			update = "UPDATE `change_rate` set VALOR = " + valor + ", date_time = '" + str(fecha_hora) + "' where NAME = '" + name + "'"
			print(update)
			conn.execute(update)
			conn.commit()
		else:
			querry = "INSERT INTO change_rate (id, NAME, VALOR, date_time) VALUES (" + str(key + 1) + ",'" + str(name) + "', " + str(valor) + ", '" + str(fecha_hora) + "')"
			print(querry)
			conn.execute(querry)
			conn.commit()
			conn.close()
			return querry

	def getURL(self,input_info, key):

		input_to = input_info[0] + ' to ' + input_info[1]
		input_t  = input_info[0] + '_' + input_info[1]

		url = 'https://www.google.com/search?q=' + input_to + '&aqs=chrome.1.69i57j35i39j0l3j69i60l3.3161j0j7&sourceid=chrome&ie=UTF-8'
		print('\n\n' + url + '\n')
		print(input_t)

		try:
			html = self.get_html(url)
			table = html.find('table')

			cite  = table.find_all('input')
			valor = cite[1].attrs['value']

			print(valor)




		except Exception as e:
			# print(e)
			pass
		self.inser_data_to_db(input_t, valor, key)

	def get_all_data(self):
		conn = sqlite3.connect('test.db')
		select = "SELECT NAME, VALOR from `change_rate`"
		data = conn.execute(select)
		data = data.fetchall()
		conn.close()
		return data

	def get_data(self, querry):

			conn = sqlite3.connect('test.db')
			data = []

			for name in querry:
				select = "SELECT NAME, VALOR from `change_rate` where NAME = '"+ name + "'"
				data_q = conn.execute(select)
				data_q = data_q.fetchall()
				print(data_q)
				# data_q = '{' + data_q[0][0] + ':'+ str(data_q[0][1]) + '}'
				q = '{0}'.format(data_q[0][0])
				v = '{0}'.format(data_q[0][1])
				data_q = {q:v}

				data.append(data_q)
			
			conn.close()
			return data


# def main():
# 	c = moneda()

# 	for i,x in enumerate([['BRL', 'COP'], ['BRL','CLP'], ['COP','BRL'], ['COP','CLP'], ['CLP','BRL'], ['CLP','COP']]):
# 		c.getURL(x, i)
	
# if __name__ == '__main__':

# 	main()