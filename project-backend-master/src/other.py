from src.data_store import data_store
import os

def clear_v1():
    store = data_store.get()
    store['users'] = []
    store['reset_code'] = []
    store['channels'] = []
    store['dm'] = []
    store['name'] = []
    store['images'] = []
    data_store.set(store)
    
    
    dir = 'static/'
    for f in os.listdir(dir):
        if f != "generic.jpg":
            os.remove(os.path.join(dir,f))
    
