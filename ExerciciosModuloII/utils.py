'''
	colocar aqui os metodos e variaveis utilitarias
'''
import os
import time 
import re


def extract_tag_content(tag_name, xml_content):
		xml_pattern = "(<"+tag_name+">.*?<\\/"+tag_name+">)"		
		return re.findall(xml_pattern,xml_content, flags = re.DOTALL)
    
def file_reader(path_to_read, encoding_to_read):
	queue_to_append = []
	with open(path_to_read, encoding = encoding_to_read) as filei:
		xml_content = filei.read()			
		for ri in extract_tag_content("RECORD", xml_content):
			try:
				title = extract_tag_content("TITLE", ri)
				abstract = extract_tag_content("ABSTRACT", ri)
				if len(abstract) == 0:
					abstract = extract_tag_content("EXTRACT", ri)
				queue_to_append.append(title[0]+abstract[0])
			except:
				pass

		return queue_to_append
	
			
def folder_reader(folder_to_read, encoding = "ISO-8859-1"):
	filenames = os.listdir(folder_to_read)
	read_time = []
	queue_to_append = []
	for fnamei in filenames:
		if "corrigido" in fnamei and not ("query" in fnamei) :
			fpathi = os.path.join(folder_to_read,fnamei)
			start_time = time.time()
			queue_to_append = queue_to_append + file_reader(fpathi, encoding)
			
			read_time.append(time.time() - start_time)													
	return (read_time, queue_to_append)

   
def query_reader(path_to_read, encoding_to_read = "ISO-8859-1"):
	with open(path_to_read, encoding = encoding_to_read) as filei:
		xml_content = filei.read()			
		return extract_tag_content("QueryText", xml_content)
		

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