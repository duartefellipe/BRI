'''
	colocar aqui os metodos e variaveis utilitarias
'''
import os
import time 
import re

def file_reader(path_to_read, encoding_to_read):
	with open(path_to_read, encoding = encoding_to_read) as filei:
		return filei.read()

def cran_reader(file_to_read, encoding = "ISO-8859-1"):
	read_time = []
	queue_to_append = []
	start_time = time.time()
	queue_to_append = re.split(".I [0-9]+\n",file_reader(file_to_read, encoding))[1:]
	read_time.append(time.time() - start_time)
													
													
	return (read_time, queue_to_append)
