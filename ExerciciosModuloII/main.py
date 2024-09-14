from utils import folder_reader, search, search_by_word
import os

if __name__ == '__main__':
	dataset_path = "../../../datasets/spa/corpus-20090418"

	index_time, spa_queue = folder_reader("/".join([dataset_path,"source", ]))
	print("Tempo total: %2.5f, Tempo medio: %2.5f de %d docs armazenados "%(sum(index_time),sum(index_time)/len(spa_queue), len(spa_queue)))

	queries_time, queries = folder_reader("/".join([dataset_path,"light", ]))
	
	search_time=[]
	for (qi_pos, qi) in enumerate(queries):
		qi_time, search_results = search(qi,spa_queue)
		search_time.append(qi_time)
		print("q%d results: "%(qi_pos), search_results)
	
	print("Tempo total: %2.5f, Tempo medio: %2.5f para buscar %d."%(sum(queries_time+search_time),(sum(queries_time)+sum(search_time))/len(queries),len(queries)))


	search_time=[]
	for (qi_pos, qi) in enumerate(queries):
		qi_time, search_results = search_by_word(qi,spa_queue)
		search_time.append(qi_time)
		print("q%d results: %d"%(qi_pos, len(search_results)))
	
	print("Tempo total: %2.5f, Tempo medio: %2.5f para buscar %d."%(sum(queries_time+search_time),(sum(queries_time)+sum(search_time))/len(queries),len(queries)))
