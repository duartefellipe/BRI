'''
	colocar aqui os metodos e variaveis utilitarias
'''
import os
import time 
def file_reader(path_to_read, encoding_to_read):
	with open(path_to_read, encoding = encoding_to_read) as filei:
		return filei.read()

def folder_reader(folder_to_read, encoding = "ISO-8859-1"):
	filenames = os.listdir(folder_to_read)
	read_time = []
	queue_to_append = []
	for fnamei in filenames:
		fpathi = "/".join([folder_to_read,fnamei])
#		print(fpathi)
		start_time = time.time()
		queue_to_append.append(file_reader(fpathi, encoding))
		read_time.append(time.time() - start_time)
													
													
	return (read_time, queue_to_append)

def search(query_to_search, data_queue):
	start_time = time.time()
	search_results = []

	for (posi, di) in enumerate(data_queue):
		if di == query_to_search:
			search_results.append(di)
			print("achou!")							
	return  (time.time() - start_time, search_results)


def search_by_word(query_to_search, data_queue):
	start_time = time.time()
	search_results = set()

	for (posi, di) in enumerate(data_queue):
		tokens = query_to_search.split(" ")
		for tki in tokens:
			if tki in query_to_search:
				search_results.add(di)							
	return  (time.time() - start_time, search_results)