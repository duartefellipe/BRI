import re, time 
import numpy as np
from io import StringIO   
from utils import file_reader, lookup
from utils import word_tokenizer, default_subquery_extractor, default_query_expansion

#_dataset_path = "../../../datasets/cranfield"
#_dataset_path = "../../../Dropbox/Arquivos BRI/Datasets/Common IR collections/cranfield"
_dataset_path = "D:/Colecoes de Dados/Common IR collections/cranfield"
_queue = []

'''
	mapeia para cada q quais documentos são esperados como resultado (i.e. a resposta correta de cada consulta)
	indice query => id do documento relevantes em _queue
'''
_golden_standard = []

'''
	indexing 
'''

def cran_reader(file_to_read, encoding = "ISO-8859-1"):
	read_time = []
	queue_to_append = []
	start_time = time.time()
	queue_to_append = re.split(".I [0-9]+\n",file_reader(file_to_read, encoding))[1:]
	read_time.append(time.time() - start_time)
	return (read_time, queue_to_append)


def read_documents():
	for i,j,k in  np.loadtxt("/".join([_dataset_path,"cranqrel"]) ,delimiter=" ", dtype=int):
		if k > 0:
			if i > len(_golden_standard):
				_golden_standard.append([])
			_golden_standard[i-1].append(j-1)
	
	index_time, _queue = cran_reader("/".join([_dataset_path,"cran.all.1400"]))
	return index_time, _queue

def preprocess(to_prep, _tokenizer = word_tokenizer):
	start_time = time.time()	
	to_prep = _tokenizer(to_prep)
	return time.time() - start_time, to_prep
	
def express_as(to_express):
	return 0, to_express
	
def _index(to_index):
	start_time = time.time()	
	_queue.append(to_index)
	return time.time() - start_time



'''
	searching
'''
def read_queries():
	return cran_reader("/".join([_dataset_path,"cran.qry"]))	
	
def extract_query(to_extract,sq_extractor=default_subquery_extractor, q_expansion = default_query_expansion):
	start_time = time.time()	
	squeries = sq_extractor(to_extract)
	for sqi_pos, sqi in enumerate(squeries):
		squeries[sqi_pos] = q_expansion(sqi)
	
	return time.time() - start_time, squeries

def _search(to_search):
	return lookup(to_search, _queue)

def rank_results(to_rank):
	return to_rank



'''
	evaluation
'''
