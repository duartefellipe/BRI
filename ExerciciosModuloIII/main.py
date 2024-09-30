import time
import spa, cranfield, cf

if __name__ == '__main__':
	
	for datasrc in [spa, cranfield, cf]:
		
		print('-'*20)
		print("Collection", datasrc.__name__)
	
		_, D = datasrc.read_documents()
		index_time = []
		for dj in D:
			pre_time, dj = datasrc.preprocess(dj, lambda x: x)
			exp_time, dj = datasrc.express_as(dj)
			
			index_time.append(pre_time + exp_time)
			index_time[-1] += datasrc._index(dj)
	
		print("Tempo total: %2.5f, Tempo medio: %2.5f de %d docs armazenados "%(sum(index_time),sum(index_time)/len(datasrc._queue), len(datasrc._queue)))
	
		_, Q = datasrc.read_queries()
	
		search_time=[]
		search_results = []
		for (qi_pos, qi) in enumerate(Q):
			pre_time, qi = datasrc.preprocess(qi, lambda x: [x])
			exp_time, SQi = datasrc.extract_query(qi)
	
			search_time.append(pre_time + exp_time)
			search_results.append([])
			
			for (sqk_pos, sqk) in enumerate(SQi):		
				retrieval_time, results = datasrc._search(sqk)
				search_time[-1] += retrieval_time
				search_results[-1]  = search_results[-1] + results
				
		print("Tempo total: %2.5f, Tempo medio: %2.5f para buscar %d."%(sum(search_time),sum(search_time)/len(Q),len(Q)))
	
		for i in range(0, len(search_results)):
	#			print("->",set(search_results[i]))
				search_results[i] = datasrc.rank_results(search_results[i])
	
		# buscando cada palavra da consulta	
		_, Q = datasrc.read_queries()
		search_time=[]
		search_results = []
		for (qi_pos, qi) in enumerate(Q):
			pre_time, qi = datasrc.preprocess(qi)
			exp_time, SQi = datasrc.extract_query(qi)
			
			search_time.append(pre_time + exp_time)
			search_results.append([])
			
			for (sqk_pos, sqk) in enumerate(SQi):		
				retrieval_time, results = datasrc._search(sqk)
				search_time[-1] += retrieval_time
				search_results[-1]  = search_results[-1] + results
		
		print("Tempo total: %2.5f, Tempo medio: %2.5f para buscar %d."%(sum(search_time),sum(search_time)/len(Q),len(Q)))
	
		for i in range(0, len(search_results)):
	#			print("->",set(search_results[i]))
				search_results[i] = datasrc.rank_results(search_results[i])
	