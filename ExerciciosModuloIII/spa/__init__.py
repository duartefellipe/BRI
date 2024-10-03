import time 
from utils import folder_reader, lookup
from utils import word_tokenizer, default_subquery_extractor, default_query_expansion

#_dataset_path = "../../../datasets/spa/corpus-20090418"
_dataset_path = "../../../Dropbox/Arquivos BRI/Datasets/short plagiarised answers corpus/corpus-20090418"

_queue = []

'''
	indexing 
'''
def read_documents():
	index_time, _queue = folder_reader("/".join([_dataset_path,"source", ]))
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
	return folder_reader("/".join([_dataset_path,"light", ]))	
	
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
