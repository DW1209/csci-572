import os
import json
from weaviate import *


if __name__ == '__main__':
    client = Client(url='http://localhost:8080/')

    # specify schema for the data we'll be using
    try:
        client.schema.delete_class('SimSearch') 
    except:
        pass

    class_obj = {
        'class': 'SimSearch',
        'vectorizer': 'text2vec-transformers'
    }
    client.schema.create_class(class_obj)

    # download data
    try:
        with open(os.path.join('inputs', 'data.json'), 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print('Error: data.json file not found...')
        exit(1)

    # send data to weaviate, to vectorize
    with client.batch as batch:
        batch.batch_size = 100
        for i, d in enumerate(data):
            print(f'\nimporting datum: {i}')
            properties = {
                'musicGenre': d['MusicGenre'],
                'songTitle': d['SongTitle'],
                'artist': d['Artist'],
            }
            print(f'properties: {properties}')
            client.batch.add_data_object(properties, 'SimSearch')
