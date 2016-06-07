""" SET and get cached files"""
import pickle


def get_file(cmpstr):
    for xx in os.listdir('.'):
        if xx.lower() == cmpstr.lower():
            return cmpstr
        else:
            return None


def get_cached():
    if get_file("dict.pkl"):
        with open("dict.pkl", 'rb') as dump_fid:
            return pickle.load(dump_fid)
    else:
        return dict()


def set_cached(dump_file):
    with open('dict.pkl', 'wb') as dump_fid:
        pickle.dump(dump_fid, dump_fid)
