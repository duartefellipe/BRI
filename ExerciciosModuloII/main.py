from utils import cran_reader, search, search_by_word
import os

if __name__ == '__main__':
	dataset_path = "../../../datasets/cranfield/"

	index_time, cran_queue = cran_reader(os.path.join(dataset_path, 'cran.all.1400'))
	print("Tempo total: %2.5f, Tempo medio: %2.5f de %d docs armazenados "%(sum(index_time),sum(index_time)/len(cran_queue), len(cran_queue)))

	queries_time, queries = cran_reader(os.path.join(dataset_path, 'cran.qry'))
	search_time=[]
	for (qi_pos, qi) in enumerate(queries):
		qi_time, search_results = search(qi,cran_queue)
		search_time.append(qi_time)
#		print("q%d results: "%(qi_pos), search_results)
		
	print("Tempo total: %2.5f, Tempo medio: %2.5f para %d consultas"%(sum(queries_time+search_time), (sum(queries_time)+sum(search_time))/len(queries), len(queries)))

	search_time=[]
	for (qi_pos, qi) in enumerate(queries):
		qi_time, search_results = search_by_word(qi,cran_queue)
		search_time.append(qi_time)
	#	print("q%d results: %d"%(qi_pos, len(search_results)))
	
	print("Tempo total: %2.5f, Tempo medio: %2.5f para %d consultas"%(sum(queries_time+search_time), (sum(queries_time)+sum(search_time))/len(queries), len(queries)))
