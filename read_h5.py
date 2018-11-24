import h5py
import json
import os
from collections import defaultdict

# global dictionary to maintain all records
artist_dict = defaultdict(list)

def read_h5(filename):
    f = h5py.File(filename, 'r')

    # dict stored for the current track
    track_dict = {}


    ##### get group object
    metadata_obj = f['metadata']
    analysis_obj = f['analysis']

    # get dataset object
    song_analysis = analysis_obj['songs']
    song_metadata = metadata_obj['songs']

    # get Dataset object from metadata
    artist_terms = list(metadata_obj['artist_terms'][()])
    artist_terms_weight = list(metadata_obj['artist_terms_weight'][()])
    # create a dict to store the pair of terms and its weight
    artist_terms_dict = {}
    for k, v in zip(artist_terms, artist_terms_weight):
        artist_terms_dict[k.decode('UTF-8')] = v
    similar_artists = list(metadata_obj['similar_artists'][()])
    similar_artists = [i.decode('UTF-8') for i in similar_artists]

    # convert scalar dataset to list
    songs = song_analysis[()]
    # convert the tuple values to list
    songs = list(songs[0])

    # get fields name as a list of a dataset
    song_attrs = list(song_analysis.dtype.fields.keys())
    # insert pair of field and values into dictionary
    song_analysis_dict = {}
    for k, v in zip(song_attrs, songs):
        song_analysis_dict[k] = v


    # get dataset object
    metadata = list(song_metadata[()][0])
    metadata_attrs = list(song_metadata.dtype.fields.keys())
    song_metadata_dict = {}
    for k, v in zip(metadata_attrs, metadata):
        song_metadata_dict[k] = v



    # # get all data into dictionary
    track_dict['track_id'] = song_analysis_dict['track_id'].decode('UTF-8')
    track_dict['tempo'] = str(song_analysis_dict['tempo'])
    track_dict['duration'] = str(song_analysis_dict['duration'])
    track_dict['artist_7digitalid'] = str(song_metadata_dict['artist_7digitalid'])
    track_dict['artist_familiarity'] = str(song_metadata_dict['artist_familiarity'])
    track_dict['artist_hotttnesss'] = str(song_metadata_dict['artist_hotttnesss'])
    track_dict['artist_id'] = song_metadata_dict['artist_id'].decode('UTF-8')
    track_dict['artist_name'] = song_metadata_dict['artist_name'].decode('UTF-8')
    track_dict['release'] = song_metadata_dict['release'].decode('UTF-8')
    track_dict['release_7digitalid'] = str(song_metadata_dict['release_7digitalid'])
    track_dict['song_hotttnesss'] = str(song_metadata_dict['song_hotttnesss'])
    track_dict['song_id'] = song_metadata_dict['song_id'].decode('UTF-8')
    track_dict['title'] = song_metadata_dict['title'].decode('UTF-8')
    track_dict['track_7digitalid'] = str(song_metadata_dict['track_7digitalid'])
    track_dict['artist_terms'] = artist_terms_dict
    track_dict['similar_artists'] = similar_artists
    # for item in track_dict.items():
    #     print(item)

    artist_dict[track_dict['artist_id']].append(track_dict)


def write_json(filename, track_dict):
    # write all JSON records for same artist
    with open(filename, 'a+') as outfile:
        json.dump(track_dict, outfile)
        outfile.write(','+'\n')


print("Start reading h5.....")
rootDir = '/Users/xinnie/Documents/CS/master/IR/Project/MillionSongSubset/data'
for dirName, subdirList, fileList in os.walk(rootDir):
    for fname in fileList:
        path = os.path.join(os.path.join(rootDir, dirName), fname)
        if not path.endswith('.h5'): continue
        else:
            print(path)
            read_h5(path)
            # print(path)
        # read_h5(path)

print('Start writing files.......')
for item in artist_dict.items():
    filename = os.path.join("/Users/xinnie/Documents/CS/master/IR/Project/artists", item[0]+'.json')
    with open(filename, 'a+') as outfile:
        outfile.write("[")
        for record in item[1]:
            json.dump(record, outfile)
            if record is not item[1][-1]: outfile.write(',' + '\n')
            else: outfile.write('\n')
            # write_json(filename, record)
        # remove last
        outfile.write(']')


