import re, time, os 
from utils import file_reader, lookup
from utils import word_tokenizer, default_subquery_extractor, default_query_expansion

#_dataset_path = "../../../datasets/cf/cfc-xml"
_dataset_path = "../../../Dropbox/Arquivos BRI/Datasets/Common IR collections/Cystic Fibrosis/cfc-xml"

_queue = []

'''
	indexing 
'''

def extract_tag_content(tag_name, xml_content):
		xml_pattern = "(<"+tag_name+">.*?<\\/"+tag_name+">)"		
		return re.findall(xml_pattern,xml_content, flags = re.DOTALL)

def cf_reader(file_to_read, encoding = "ISO-8859-1"):
	read_time = []
	queue_to_append = []
	start_time = time.time()
	
	xml_content = file_reader(file_to_read, encoding)
	for ri in extract_tag_content("RECORD", xml_content):
			try:
				title = extract_tag_content("TITLE", ri)
				abstract = extract_tag_content("ABSTRACT", ri)
				if len(abstract) == 0:
					abstract = extract_tag_content("EXTRACT", ri)
				queue_to_append.append(title[0]+abstract[0])
			except:
				pass	
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
		start_time = time.time()	
		xml_content = file_reader(os.path.join(_dataset_path,"cfquery-corrigido.xml"), "ISO-8859-1")
		return (time.time() - start_time, extract_tag_content("QueryText", xml_content))
	
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
