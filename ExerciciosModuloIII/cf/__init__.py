import re, time, os 
from utils import file_reader, lookup
from utils import word_tokenizer, default_subquery_extractor, default_query_expansion

#_dataset_path = "../../../datasets/cf/cfc-xml"
#_dataset_path = "../../../Dropbox/Arquivos BRI/Datasets/Common IR collections/Cystic Fibrosis/cfc-xml"
_dataset_path = "D:/Colecoes de Dados/Common IR collections/Cystic Fibrosis/cfc-xml"
_queue = []

'''
	mapeia o RECORDNUM de cada documento para o indice do seu texto em _queue
	RECORDNUM => inteiro
'''
_rn_to_queue = {}

'''
	mapeia para cada q quais documentos são esperados como resultado (i.e. a resposta correta de cada consulta)
	indice query => id do documento relevantes em _queue
'''
_golden_standard = []


'''
	indexing 
'''

def extract_tag_content(tag_name, xml_content):
		xml_pattern = "<"+tag_name+">(.*?)<\\/"+tag_name+">"	
		return re.findall(xml_pattern,xml_content, flags = re.DOTALL)

def cf_reader(file_to_read, encoding = "ISO-8859-1"):
	read_time = []
	queue_to_append = []
	start_time = time.time()
	
	xml_content = file_reader(file_to_read, encoding)
	for ri in extract_tag_content("RECORD", xml_content):
		try:	
			record_number =  int(re.findall(r'\d+', extract_tag_content("RECORDNUM", ri)[0])[0])
		except:
			continue
		_rn_to_queue[record_number] = len(queue_to_append)			
		title = extract_tag_content("TITLE", ri)
		abstract = extract_tag_content("ABSTRACT", ri)
		if len(abstract) == 0:
			abstract = extract_tag_content("EXTRACT", ri)
		queue_to_append.append(title[0]+abstract[0])

	read_time.append(time.time() - start_time)
	return (read_time, queue_to_append)


def read_documents():
	filenames = os.listdir(_dataset_path)
	read_time = []
	queue_to_append = []
	for fnamei in filenames:
		if "corrigido" in fnamei and not ("query" in fnamei) :
			fpathi = os.path.join(_dataset_path,fnamei)
			start_time = time.time()
			_, to_append = cf_reader(fpathi)
			queue_to_append = queue_to_append + to_append
			
			read_time.append(time.time() - start_time)													
	return (read_time, queue_to_append)	

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
	
	start_time = time.time()	
	xml_content = file_reader(os.path.join(_dataset_path,"cfquery-corrigido.xml"), "ISO-8859-1")
		
	queries_text = extract_tag_content("QueryText", xml_content)
	queries_records = extract_tag_content("Records", xml_content)
		
	for qri in queries_records:
		_golden_standard.append([_rn_to_queue[int(s)] for s in re.findall(r'>(\b\d+\b)<', qri)])
		
	return (time.time() - start_time, queries_text)
	
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
