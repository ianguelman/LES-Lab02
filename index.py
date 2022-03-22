from concurrent.futures import process
from scripts.query import run as query
from scripts.execute import run as execute
from utils.mongo import Mongo
from threading import Thread

query()

threads = 24
documents = Mongo().get_all_documents()

def loop(start, stop):
    for i in range(start, stop):
        if not documents[i]['processed']:
            execute(documents[i]['url'])
            
size = len(documents) / threads

for i in range(threads):
    args = (int(size * i), int(size * i + size -1)) if i != threads - 1 else (int(size * i), int(size * i + size))
    t = Thread(target = loop, args = args)
    t.start()
    




