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


def search(query_to_search, data_queue):
	start_time = time.time()
	search_results = []

	for (posi, di) in enumerate(data_queue):
		if di == query_to_search:
			search_results.append(posi)
	return  (time.time() - start_time, search_results)


def search_by_word(query_to_search, data_queue):
	start_time = time.time()
	search_results = set()

	for (posi, di) in enumerate(data_queue):
		tokens = query_to_search.split(" ")
		for tki in tokens:
			if tki in query_to_search:
				search_results.add(posi)							
	return  (time.time() - start_time, search_results)