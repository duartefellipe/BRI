import time
import spa, cranfield, cf
import utils
from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.lancaster import LancasterStemmer

if __name__ == '__main__':
	tokenizer_list = [
			utils.word_tokenizer, #tokenizando pelo espaco 
			utils.tokenizerFactory( utils._RG_SPACES +"|"+utils._RG_PUNCTUATION), #tokenizando pelo espaco e pela pontuação
			utils.tokenizerFactory( utils._RG_SPACES +"|"+utils._RG_PUNCTUATION, True), #tokenizando pelo espaco e pela pontuação; colocando tudo em letra minuscula
			utils.tokenizerFactory( utils._RG_SPACES +"|"+utils._RG_PUNCTUATION, True, utils._RG__SPECIALCHAR+"|"+utils._RG__NUMBER), #tokenizando pelo espaco e pela pontuação; colocando tudo em letra minuscula; removendo numeros e caracteres especiais
			utils.tokenizerFactory( utils._RG_SPACES +"|"+utils._RG_PUNCTUATION, True, utils._RG__SPECIALCHAR+"|"+utils._RG__NUMBER, utils._STOPLIST), #tokenizando pelo espaco e pela pontuação; colocando tudo em letra minuscula; removendo numeros, caracteres especiais e uma pequena lista de stopwords
			
			utils.tokenizerFactory( utils._RG_SPACES +"|"+utils._RG_PUNCTUATION, True, utils._RG__SPECIALCHAR+"|"+utils._RG__NUMBER, utils._STOPLIST,stemmer=PorterStemmer()), #tokenizando pelo espaco e pela pontuação; colocando tudo em letra minuscula; removendo numeros, caracteres especiais e uma pequena lista de stopwords
			utils.tokenizerFactory( utils._RG_SPACES +"|"+utils._RG_PUNCTUATION, True, utils._RG__SPECIALCHAR+"|"+utils._RG__NUMBER, utils._STOPLIST,stemmer=SnowballStemmer("english")), #tokenizando pelo espaco e pela pontuação; colocando tudo em letra minuscula; removendo numeros, caracteres especiais e uma pequena lista de stopwords
			utils.tokenizerFactory( utils._RG_SPACES +"|"+utils._RG_PUNCTUATION, True, utils._RG__SPECIALCHAR+"|"+utils._RG__NUMBER, utils._STOPLIST,stemmer= LancasterStemmer()), #tokenizando pelo espaco e pela pontuação; colocando tudo em letra minuscula; removendo numeros, caracteres especiais e uma pequena lista de stopwords
			]	
	for datasrc in [spa,
	cranfield,
	cf
	]:
		for tokenizeri in tokenizer_list:
			print('-'*20)
			print("Colecao:", datasrc.__name__)
			_, D = datasrc.read_documents()
			datasrc._queue = []
			index_time = []
			for dj in D:
				pre_time, dj = datasrc.preprocess(dj, utils.word_tokenizer)
				exp_time, dj = datasrc.express_as(dj)
				
				index_time.append(pre_time + exp_time)
				index_time[-1] += datasrc._index(dj)
		
			print("--Tempo total: %2.5f, Tempo medio: %2.5f de %d docs armazenados "%(sum(index_time),sum(index_time)/len(datasrc._queue), len(datasrc._queue)))
			
			
			for ngram_range in [1,2,3,5]:
				_, Q = datasrc.read_queries()
				search_time=[]
				search_results = []
				search_results_count = []
				print("--Buscando consultas de %d palavras (%d-grams)"%(ngram_range,ngram_range))
				for (qi_pos, qi) in enumerate(Q):
					pre_time, qi = datasrc.preprocess(qi, tokenizeri)
					subqueries = utils.subquery_factory(ngram_range)
					
					exp_time, SQi = datasrc.extract_query(qi, subqueries)
					
					search_time.append(pre_time + exp_time)
					search_results.append([])
					
					for (sqk_pos, sqk) in enumerate(SQi):		
						retrieval_time, results = datasrc._search(sqk)
						search_time[-1] += retrieval_time
						search_results[-1]  = search_results[-1] + results
		#				print(sqk)
		#				print(results)
			#		print(search_results[-1])
				
						
					search_results_count.append(len(set(search_results[-1])))
				
				print("--Tempo total: %2.5f, Tempo medio: %2.5f para buscar %d."%(sum(search_time),sum(search_time)/len(Q),len(Q)))
				print(">>>Media retornados/consulta: %2.0f"%(sum(search_results_count)/len(Q)))
			

'''		
				for i in range(0, len(search_results)):
						search_results[i] = datasrc.rank_results(search_results[i])
		
'''