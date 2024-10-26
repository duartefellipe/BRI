import os
import time 
import re
from nltk.probability import FreqDist
import numpy as np

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
	
def lookup(what_look, where_look, how_look):
	start_time = time.time()
	search_results = []

	for (posi, di) in enumerate(where_look):
		if how_look == "boolean":
			if len(set(what_look) & set(di))  == len(set(what_look) ):
				search_results.append(posi)
		elif how_look == "VSM":
			if len(set(what_look) & set(di))  > 0 :
				search_results.append(posi)
		else:
			raise NotImplementedError
				
	return  (time.time() - start_time, search_results)

def jaccard_sim(set_a, set_b):
	return len(set_a & set_b)/(len(set_a) + len(set_b)-len(set_a & set_b))

def cossine_sim(v1, v2):
	v1_fd = FreqDist(v1)
	v2_fd = FreqDist(v2)
	
	v1_v2_sim = 0
	for v1_token, tk_weight in v1_fd.items():
		v1_v2_sim += tk_weight*v2_fd[v1_token]
				
	v1_v2_sim /= (v1_fd.N() * v2_fd.N()) 
	
	return v1_v2_sim


def retrieve_top_k(query, to_rank, ir_model, k, _queue):
	scores = []
	if k == None:
		k = len(_queue)
	
	start_time = time.time()	
	if ir_model == "boolean":
		q = set(query)
		for i in to_rank:
			di = set(_queue[i])
			scores.append(jaccard_sim(q,di))
	elif ir_model == "VSM":
		for i in to_rank:
			scores.append(cossine_sim(query, _queue[i]))
	else:
		raise NotImplementedError

	scores = np.array(scores)
	scores_order = (np.argsort(scores)[::-1])
	
	sorted_results = (np.array(to_rank)[scores_order])
	
# 	print(k,sorted_results.tolist()[0:k])
	return time.time() - start_time, sorted_results.tolist()[0:k]


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
	str_tokens = [i for i in re.split(token_pattern,str_to_tokenize) if i not in stoplist]
	
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

