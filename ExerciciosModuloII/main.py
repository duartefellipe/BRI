from utils import  search, search_by_word, folder_reader, query_reader
import os

if __name__ == '__main__':
	dataset_path = "../../../../Dropbox/Arquivos BRI/Datasets/Common IR collections/Cystic Fibrosis/cfc-xml"

	index_time, cf_queue = folder_reader(dataset_path)
	print("Tempo total: %2.5f, Tempo medio: %2.5f de %d docs armazenados "%(sum(index_time),sum(index_time)/len(cf_queue), len(cf_queue)))


	queries = query_reader(os.path.join(dataset_path, "cfquery-corrigido.xml"))
	search_time=[]
	for (qi_pos, qi) in enumerate(queries):
		qi_time, search_results = search(qi,cf_queue)
		search_time.append(qi_time)
#		print("q%d results: "%(qi_pos), search_results)
		
	print("Tempo total: %2.5f, Tempo medio: %2.5f para %d consultas"%(sum(search_time), sum(search_time)/len(queries), len(queries)))

	search_time=[]
	for (qi_pos, qi) in enumerate(queries):
		qi_time, search_results = search_by_word(qi,cf_queue)
		search_time.append(qi_time)
	#	print("q%d results: %d"%(qi_pos, len(search_results)))
	
print("Tempo total: %2.5f, Tempo medio: %2.5f para %d consultas"%(sum(search_time), sum(search_time)/len(queries), len(queries)))