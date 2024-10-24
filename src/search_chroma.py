import chromadb
import numpy as np
from pathlib import Path
from . import io_local
import os
import pandas as pd

def chunk_by_len(text, sp='\n', chunk_size=500):
    lines = text.split(sp)  # default by newline/paragraph
    chunks = []
    current_chunk = ""

    for line in lines:
        if len(current_chunk) + len(line) <= chunk_size:
            current_chunk += line + '\n'
        else:
            chunks.append(current_chunk.strip())
            current_chunk = line + '\n'
    # Append the last chunk
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks


def sync_dir(collection, root_dir, chunk_fn=None):
    ''' 
        Synchronize directory into collection. 
            - 1. Local files if not in DB, and newer: add or update
            - 2. DB files delete if file not exist
            - 3. Metadata : {'path', 'type', 'size', 'date'}
    '''
    ## file-meta and db-meta DataFrame
    f_metas = io_local.list_dir_metas(root_dir)
    db_info = collection.get(include=['metadatas']) # raw
    db_metas = pd.DataFrame(db_info['metadatas'])
    db_metas['ids'] = db_info['ids']
    
    ## add
    f_add = f_metas[~f_metas.path.isin(db_metas.path.unique())].path

    ## update
    merged_df = pd.merge(f_metas, db_metas, on='path', suffixes=('_a', '_b'))
    f_up = merged_df[merged_df['date_a'] > merged_df['date_b']].path.unique()

    chunks = chunk_len
    collection.add(documents = [io_local.read_file(f) for f in f_add],
                  ids=f_add,
                  metadatas=f_metas[f_metas.path.isin(f_add)])

    ## update
    
    ## delete
    db_delete = [ m['ids'] for m in db_metas if not os.path.isfile(m['path']) ]
    if len(db_delete) > 0:
        collection.delete(ids = db_delete)

    return f_metas_update, db_delete


def search_context(search_text:str, collection, top=5) -> dict:
    '''
        search the files from local database(chromadb)
        args:
            - search_text: the search(query) str
            - collection: the chromadb collection
            - top: number results to return
        return:
            results of query
    '''
    # setup Chroma in-memory, for easy prototyping. Can add persistence easily!
    return collection.query(query_texts = search_text,  n_results=top)


    
