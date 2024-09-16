from utils import cran_reader
import os

if __name__ == '__main__':
	dataset_path = "../../../datasets/cranfield/cran.all.1400"

	index_time, cran_queue = cran_reader(dataset_path)
	print("Tempo total: %2.5f, Tempo medio: %2.5f de %d docs armazenados "%(sum(index_time),sum(index_time)/len(cran_queue), len(cran_queue)))

