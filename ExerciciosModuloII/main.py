from utils import folder_reader
import os

if __name__ == '__main__':
	dataset_path = "../../../datasets/spa/corpus-20090418"

	index_time, spa_queue = folder_reader("/".join([dataset_path,"source", ]))
	print("Tempo total: %2.5f, Tempo medio: %2.5f de %d docs armazenados "%(sum(index_time),sum(index_time)/len(spa_queue), len(spa_queue)))
