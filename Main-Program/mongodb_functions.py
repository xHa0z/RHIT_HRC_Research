import pymongo
from pymongo import MongoClient
from pymongo import DeleteMany, DeleteOne
from datetime import datetime
import sys

client = MongoClient();
db = client.HRC;

def insert_game(game_num):
    games = db['games']
    current_time = datetime.now()
    game = {'game_num': game_num,
            'timestampe': current_time}
    result = games.insert_one(game).inserted_id
    print result

def delete_game(game_num):
    games = db['games']
    cursor = games.find({'game_num':game_num})
    if(cursor.count() == 1):
        result = games.delete_one({'game_num' : game_num})
        print result.deleted_count
        delete_transcripts(game_num)
        delete_leap_motion(game_num)
    else:
        print 'no such game'
    print cursor.count()



def insert_transcript(game_num, transcription):
    curosr = db.games.find({'game_num':game_num})
    if (curosr.count() == 1):
        transcriptions = db['transcriptions']
        current_time = datetime.now()
        transcript = {'game_num':game_num,
                      'transcription':transcription,
                      'timestamp':current_time}
        result = transcriptions.insert_one(transcript).inserted_id
        print result
    else:
        print 'no such game to insert transcript'

def delete_transcripts(game_num):
    transcriptions = db['transcriptions']
    request = [DeleteMany({'game_num': game_num})]
    result = transcriptions.bulk_write(request)
    print result.deleted_count

def insert_leap_motion(game_num, data):
    curosr = db.games.find({'game_num': game_num})
    if (curosr.count() == 1):
        matrices = db['matrices']
        current_time = datetime.now()
        matrix = {'game_num':game_num,
                  'matrix':data,
                  'timestamp':current_time}
        result = matrices.insert_one(matrix).inserted_id
        print result
    else:
        print 'no such game to insert transcript'

def delete_leap_motion(game_num):
    matrices = db['matrices']
    request = [DeleteMany({'game_num': game_num})]
    result = matrices.bulk_write(request)
    print result.deleted_count


