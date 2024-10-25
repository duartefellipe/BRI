import time
import spa, cranfield, cf
import utils
from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.lancaster import LancasterStemmer
from nltk.probability import FreqDist
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
	tokenizer_list = [
			utils.word_tokenizer,
#			utils.tokenizerFactory( utils._RG_SPACES +"|"+utils._RG_PUNCTUATION, True, utils._RG__SPECIALCHAR+"|"+utils._RG__NUMBER), #tokenizando pelo espaco e pela pontuação; colocando tudo em letra minuscula; removendo numeros e caracteres especiais
#			utils.tokenizerFactory( utils._RG_SPACES +"|"+utils._RG_PUNCTUATION, True, utils._RG__SPECIALCHAR+"|"+utils._RG__NUMBER, utils._STOPLIST), #tokenizando pelo espaco e pela pontuação; colocando tudo em letra minuscula; removendo numeros, caracteres especiais e uma pequena lista de stopwords
#			utils.tokenizerFactory( utils._RG_SPACES +"|"+utils._RG_PUNCTUATION, True, utils._RG__SPECIALCHAR+"|"+utils._RG__NUMBER, utils._STOPLIST,stemmer=PorterStemmer()), #tokenizando pelo espaco e pela pontuação; colocando tudo em letra minuscula; removendo numeros, caracteres especiais e uma pequena lista de stopwords
			]	
	for datasrc in [spa,
	cranfield,
	cf
	]:
		for tokenizeri in tokenizer_list:
			print('-'*25)
			print("Colecao:", datasrc.__name__)
			_, D = datasrc.read_documents()
			_, Q = datasrc.read_queries()
			N = len(D) + len(Q)
			print("- %d documentos!"%(N))
						
			fd = FreqDist()
			for text_src in [D,Q]:
				for d in text_src:
					_, d = datasrc.preprocess(d, tokenizeri)
					for word in d:
						fd[word] += 1

			y_range = 100
			p = fd.plot(y_range,show=False,title="Distribuição das palavras no corpus %s"%(datasrc.__name__))
			p.set_xlabel("Amostra")
			p.set_ylabel("Frequência")
			plots =[]
			labels = []

			for j in range(0,5,2):
				C = fd[fd.max()]*(1.0+j/10)
				
				for alpha in [0.5, 1]:
					n_r = [C*(i**(-alpha)) for i in range(1, y_range+1)]
					p1, = plt.plot(n_r, linestyle = 'dotted')
					plots.append(p1)
					labels.append("C=%4.2f,alfa=%1.2f"%(C, alpha))
			
			plt.legend(plots, labels, loc=1)
			plt.show()
	
		relevants_count = [len(i) for i in datasrc._golden_standard]
		print(">>>Media relevantes/consulta: %2.0f"%(np.mean(relevants_count)))
		
		plt.scatter(range(0,len(datasrc._golden_standard)), relevants_count, marker='.')
		plt.title("Número de relevantes x consultas no corpus %s"%(datasrc.__name__))
		plt.ylabel("numero de relevantes")
		plt.xlabel("id da consulta")
# 		plt.ylim=(0,5)
		plt.show()