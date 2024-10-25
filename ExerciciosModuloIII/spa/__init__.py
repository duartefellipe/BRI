import time, os, re 
from utils import folder_reader, lookup
from utils import word_tokenizer, default_subquery_extractor, default_query_expansion

#_dataset_path = "../../../datasets/spa/corpus-20090418"
# _dataset_path = "../../../Dropbox/Arquivos BRI/Datasets/short plagiarised answers corpus/corpus-20090418"
_dataset_path = "D:/Colecoes de Dados/short plagiarised answers corpus/corpus-20090418"

_queue = []

'''
	mapeia o nome da tarefa de cada documento para o indice do seu texto em _queue
'''
_tn_to_queue = []

'''
	mapeia para cada q quais documentos são esperados como resultado (i.e. a resposta correta de cada consulta)
	indice query => id do documento relevantes em _queue
'''
_golden_standard = []

'''
	indexing 
'''
def read_documents():
	global _tn_to_queue
	folder_to_read  = "/".join([_dataset_path,"source", ])
	_tn_to_queue = os.listdir(folder_to_read)
	index_time, _queue = folder_reader(folder_to_read)
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
	global _golden_standard
	_golden_standard = []
	folder_to_read = "/".join([_dataset_path,"light", ])
	
	for qpos, q in enumerate(os.listdir(folder_to_read)):
		q_src_id = _tn_to_queue.index(re.sub("(g.*)_", "orig_",q))
		_golden_standard.append([q_src_id])
	
	return folder_reader(folder_to_read)	
	
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
