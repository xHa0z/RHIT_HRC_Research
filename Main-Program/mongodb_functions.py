import pymongo
from pymongo import MongoClient
from pymongo import DeleteMany, DeleteOne
from datetime import datetime
import sys
import gridfs
from bson import Binary

client = MongoClient('137.112.97.32:27017');
db = client.HRC;
fs = gridfs.GridFS(db)

def insert_game(game_num):
    games = db['games']
    cursor = games.find({'game_num':game_num})
    if cursor.count() == 0:
        current_time = datetime.now()
        game = {'game_num': game_num,
                'timestampe': current_time}
        result = games.insert_one(game).inserted_id
        print 'insert game id' + str(result)
    else:
        print 'game exists'

def delete_game(game_num):
    games = db['games']
    cursor = games.find({'game_num':game_num})
    if(cursor.count() == 1):
        result = games.delete_one({'game_num' : game_num})
        print 'game delete # ' + str(result.deleted_count)
        delete_video_path(game_num)
        delete_game_matrix(game_num)
        delete_transcripts(game_num)
        delete_leap_motion_raw(game_num)
        delete_leap_motion_result(game_num)
        delete_nlp_matrix(game_num)
        delete_decision_matrix(game_num)
        delete_decision_index(game_num)
        delete_button_selection(game_num)
    else:
        print 'no such game'
    print cursor.count()
    
def insert_video_dir(game_num, path):
    curosr = db.games.find({'game_num': game_num})
    if (curosr.count() == 1):
        dirctories = db['directories']
        current_time = datetime.now()
        path = {'game_num':game_num,
                  'path':path,
                  'timestamp':current_time}
        result = dirctories.insert_one(path).inserted_id
        print 'insert game path id ' + str(result)
    else:
        print 'no such game path to insert db'
        
def delete_video_path(game_num):
    matrices = db['matrices']
    request = [DeleteMany({'game_num': game_num,
                           'source':'game'})]
    result = matrices.bulk_write(request)
    print 'delete game matrix # ' + str(result.deleted_count)    

def insert_game_matrix(game_num, data):
    curosr = db.games.find({'game_num': game_num})
    if (curosr.count() == 1):
        matrices = db['matrices']
        current_time = datetime.now()
        matrix = {'game_num':game_num,
                  'source':'game',
                  'matrix':data,
                  'timestamp':current_time}
        result = matrices.insert_one(matrix).inserted_id
        print 'insert game matrix id ' + str(result)
    else:
        print 'no such game matrix to insert db'
        
def delete_game_matrix(game_num):
    matrices = db['matrices']
    request = [DeleteMany({'game_num': game_num,
                           'source':'game'})]
    result = matrices.bulk_write(request)
    print 'delete game matrix # ' + str(result.deleted_count)

def insert_transcript(game_num, transcription):
    curosr = db.games.find({'game_num':game_num})
    if (curosr.count() == 1):
        transcriptions = db['transcriptions']
        current_time = datetime.now()
        transcript = {'game_num':game_num,
                      'transcription':transcription,
                      'timestamp':current_time}
        result = transcriptions.insert_one(transcript).inserted_id
        print 'insert transcript id' + str(result)
    else:
        print 'no such transcript to insert into db'

def delete_transcripts(game_num):
    transcriptions = db['transcriptions']
    request = [DeleteMany({'game_num': game_num})]
    result = transcriptions.bulk_write(request)
    print 'delete transcripts # ' + str(result.deleted_count)

def insert_leap_motion_raw(game_num, data):
    curosr = db.games.find({'game_num': game_num})
    if (curosr.count() == 1):
        matrices = db['matrices']
        current_time = datetime.now()
        matrix = {'game_num':game_num,
                  'source':'leap_motion_raw',
                  'matrix':data,
                  'timestamp':current_time}
        result = matrices.insert_one(matrix).inserted_id
        print 'insert leap_motion_raw id' + str(result)
    else:
        print 'no such leap motion raw to insert into db'

def delete_leap_motion_raw(game_num):
    matrices = db['matrices']
    request = [DeleteMany({'game_num': game_num,
                           'source':'leap_motion_raw'})]
    result = matrices.bulk_write(request)
    print 'delete leap motion raw # ' + str(result.deleted_count)

def insert_leap_motion_result(game_num, data):
    curosr = db.games.find({'game_num': game_num})
    if (curosr.count() == 1):
        matrices = db['matrices']
        current_time = datetime.now()
        matrix = {'game_num':game_num,
                  'source':'leap_motion_result',
                  'matrix':data,
                  'timestamp':current_time}
        result = matrices.insert_one(matrix).inserted_id
        print 'isnert leap motion result id ' + str(result)
    else:
        print 'no such leap motion result to insert into db'
        
        
def delete_leap_motion_result(game_num):
    matrices = db['matrices']
    request = [DeleteMany({'game_num': game_num,
                           'source':'leap_motion_result'})]
    result = matrices.bulk_write(request)
    print 'delete leap motion result # ' + str(result.deleted_count)

def insert_nlp_matrix(game_num, data):
    curosr = db.games.find({'game_num': game_num})
    if (curosr.count() == 1):
        matrices = db['matrices']
        current_time = datetime.now()
        matrix = {'game_num':game_num,
                  'source':'nlp_result',
                  'matrix':str(data),
                  'timestamp':current_time}
        result = matrices.insert_one(matrix).inserted_id
        print 'inert nlp matrxi id ' + str(result)
    else:
        print 'no such nlp to insert into db'
        
def delete_nlp_matrix(game_num):
    matrices = db['matrices']
    request = [DeleteMany({'game_num': game_num,
                           'source':'nlp_result'})]
    result = matrices.bulk_write(request)
    print 'delete nlp matrix # ' + str(result.deleted_count)
    
def insert_decision_matrix(game_num, data):
    curosr = db.games.find({'game_num': game_num})
    if (curosr.count() == 1):
        matrices = db['matrices']
        current_time = datetime.now()
        matrix = {'game_num':game_num,
                  'source':'decision_matrix',
                  'matrix':data,
                  'timestamp':current_time}
        result = matrices.insert_one(matrix).inserted_id
        print 'insert decision matrix id ' + str(result)
    else:
        print 'no such decision matrix to insert into db'
        
def delete_decision_matrix(game_num):
    matrices = db['matrices']
    request = [DeleteMany({'game_num': game_num,
                           'source':'decision_matrix'})]
    result = matrices.bulk_write(request)
    print 'delete decision matrix # ' + str(result.deleted_count)
    
def insert_decision_index(game_num, data):
    curosr = db.games.find({'game_num': game_num})
    if (curosr.count() == 1):
        matrices = db['matrices']
        current_time = datetime.now()
        matrix = {'game_num':game_num,
                  'source':'decision_index',
                  'matrix':data,
                  'timestamp':current_time}
        result = matrices.insert_one(matrix).inserted_id
        print 'insert decision index id ' + str(result)
    else:
        print 'no such decision index to insert into db'
        
def delete_decision_index(game_num):
    matrices = db['matrices']
    request = [DeleteMany({'game_num': game_num,
                           'source':'decision_index'})]
    result = matrices.bulk_write(request)
    print 'delete decision index # ' + str(result.deleted_count)
    
def insert_button_selection(game_num, data):
    curosr = db.games.find({'game_num': game_num})
    if (curosr.count() == 1):
        buttons = db['buttons']
        current_time = datetime.now()
        button = {'game_num':game_num,
                  'selection':data,
                  'timestamp':current_time}
        result = buttons.insert_one(button).inserted_id
        print 'insert button selection id ' + str(result)
    else:
        print 'no such decision index to insert into db'
        
def delete_button_selection(game_num):
    buttons = db['buttons']
    request = [DeleteMany({'game_num': game_num})]
    result = buttons.bulk_write(request)
    print 'delete buttons # ' + str(result.deleted_count)