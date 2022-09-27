import pickle
import random
import subprocess


def loadData(file):
    dbfile = open(file, 'rb')
    db = pickle.load(dbfile)
    for keys in db:
        print(keys, '=>', db[keys])
    dbfile.close()

def delete(file):
    subprocess.run(["rm", file])