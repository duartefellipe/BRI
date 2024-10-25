import os
import time 
import re

'''
	colocar aqui os metodos e variaveis utilitarias
'''
def file_reader(path_to_read, encoding_to_read):
	with open(path_to_read, encoding = encoding_to_read) as filei:
		return filei.read()

def folder_reader(folder_to_read, encoding = "ISO-8859-1"):
	filenames = os.listdir(folder_to_read)
	read_time = []
	queue_to_append = []
	for fnamei in filenames:
		fpathi = "/".join([folder_to_read,fnamei])
		
		start_time = time.time()
		queue_to_append.append(file_reader(fpathi, encoding))
		read_time.append(time.time() - start_time)
	return (read_time, queue_to_append)
	
def lookup(what_look, where_look):
	start_time = time.time()
	search_results = []

	for (posi, di) in enumerate(where_look):
		if len(set(what_look) & set(di))  == len(set(what_look) ):
			search_results.append(posi)

	return  (time.time() - start_time, search_results)


def eval_result(query_results, _golden_standard, metric_name):
	results_eval = []
	for q_id, q_res in enumerate(query_results):
		a = set(q_res)
		b = set(_golden_standard[q_id])
		a_b = a.intersection(b)
		
		try:
			if metric_name == "precision":
				results_eval.append(len(a_b)/len(a))
			else:
				results_eval.append(len(a_b)/len(b))
		except ZeroDivisionError as e:
			results_eval.append(0)
						
	return results_eval

def eval_precision(query_results, _golden_standard):
	return eval_result(query_results, _golden_standard, "precision")

def eval_recall(query_results, _golden_standard):
	return eval_result(query_results, _golden_standard, "recall")

def default_query_expansion(query):
	return query

_STOPLIST = {"the", "a", "an", "is", "of", "with", "and", "or", "to", "it", "in", "at", "as", "on", "by", "be", "any", "not", "also"}
_RG_SPACES  = "\s+"
_RG_PUNCTUATION  = "[,\\.!\\?]"
_RG__NUMBER  =  " [0-9]+([\.,][0-9]+)*"
_RG__SPECIALCHAR =  "[^\w\s]"

def regex_tokenizer(str_to_tokenize, token_pattern, to_lowercase, clean_pattern, stoplist, stemmer):
	if to_lowercase:
		str_to_tokenize = str_to_tokenize.lower()
	
	str_to_tokenize = re.sub(clean_pattern, "",  str_to_tokenize).strip()
	str_tokens = set(re.split(token_pattern,str_to_tokenize))
	str_tokens = str_tokens - stoplist	
	if stemmer != None:
		str_tokens = list(map(stemmer.stem,str_tokens))
	return list(str_tokens)
	
def tokenizerFactory( token_pattern= _RG_SPACES, to_lowercase=False, clean_pattern= "", stoplist = set(),stemmer = None):
	def new_tokenizer(str_to_tokenize):
		return regex_tokenizer(str_to_tokenize, token_pattern, to_lowercase, clean_pattern, stoplist, stemmer)		
	return new_tokenizer

word_tokenizer = tokenizerFactory( _RG_SPACES)


def subquery_extractor(query, ngram_range=1):
	sub_queries = []
	for i in range(0,len(query),ngram_range):
		sub_queries.append(query[i:i+ngram_range])
		
	return sub_queries

def subquery_factory(ngram_range=1):
	def new_subquery_extractor(query):
		return subquery_extractor(query, ngram_range)
				
	return new_subquery_extractor

default_subquery_extractor = subquery_factory()

