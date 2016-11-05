#!/usr/bin/python
# Copyright (C) 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Sample that streams audio to the Google Cloud Speech API via GRPC."""

from __future__ import division
from __future__ import print_function

import contextlib
import re
import signal
import threading
import json
import os
import datetime
import sys
import datetime


import numpy as np

from google.cloud import credentials
from google.cloud.speech.v1beta1 import cloud_speech_pb2 as cloud_speech
from google.rpc import code_pb2
from grpc.beta import implementations
from grpc.framework.interfaces.face import face
import pyaudio
from six.moves import queue

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

# The Speech API has a streaming limit of 60 seconds of audio*, so keep the
# connection alive for that long, plus some more to give the API time to figure
# out the transcription.
# * https://g.co/cloud/speech/limits#content
DEADLINE_SECS = 60 * 10 + 5
SPEECH_SCOPE = 'https://www.googleapis.com/auth/cloud-platform'



# game board, 0 - nothing, 1 - red, 2 - green, 3 - blue
game = np.loadtxt('game.txt', dtype = 'int')

print (game)




def make_channel(host, port):
    """Creates an SSL channel with auth credentials from the environment."""
    # In order to make an https call, use an ssl channel with defaults
    ssl_channel = implementations.ssl_channel_credentials(None, None, None)

    # Grab application default credentials from the environment
    creds = credentials.get_credentials().create_scoped([SPEECH_SCOPE])
    # Add a plugin to inject the creds into the header
    auth_header = (
        'Authorization',
        'Bearer ' + creds.get_access_token().access_token)
    auth_plugin = implementations.metadata_call_credentials(
        lambda _, cb: cb([auth_header], None),
        name='google_creds')

    # compose the two together for both ssl and google auth
    composite_channel = implementations.composite_channel_credentials(
        ssl_channel, auth_plugin)

    return implementations.secure_channel(host, port, composite_channel)


def _audio_data_generator(buff):
    """A generator that yields all available data in the given buffer.
    Args:
        buff - a Queue object, where each element is a chunk of data.
    Yields:
        A chunk of data that is the aggregate of all chunks of data in `buff`.
        The function will block until at least one data chunk is available.
    """
    while True:
        # Use a blocking get() to ensure there's at least one chunk of data
        chunk = buff.get()
        if not chunk:
            # A falsey value indicates the stream is closed.
            break
        data = [chunk]

        # Now consume whatever other data's still buffered.
        while True:
            try:
                data.append(buff.get(block=False))
            except queue.Empty:
                break
        yield b''.join(data)


def _fill_buffer(audio_stream, buff, chunk):
    """Continuously collect data from the audio stream, into the buffer."""
    try:
        while True:
            buff.put(audio_stream.read(chunk))
    except IOError:
        # This happens when the stream is closed. Signal that we're done.
        buff.put(None)


# [START audio_stream]
@contextlib.contextmanager
def record_audio(rate, chunk):
    """Opens a recording stream in a context manager."""
    audio_interface = pyaudio.PyAudio()
    audio_stream = audio_interface.open(
        format=pyaudio.paInt16,
        # The API currently only supports 1-channel (mono) audio
        # https://goo.gl/z757pE
        channels=1, rate=rate,
        input=True, frames_per_buffer=chunk,
    )

    # Create a thread-safe buffer of audio data
    buff = queue.Queue()

    # Spin up a separate thread to buffer audio data from the microphone
    # This is necessary so that the input device's buffer doesn't overflow
    # while the calling thread makes network requests, etc.
    fill_buffer_thread = threading.Thread(
        target=_fill_buffer, args=(audio_stream, buff, chunk))
    fill_buffer_thread.start()

    yield _audio_data_generator(buff)

    audio_stream.stop_stream()
    audio_stream.close()
    fill_buffer_thread.join()
    audio_interface.terminate()
# [END audio_stream]


def request_stream(data_stream, rate):
    """Yields `StreamingRecognizeRequest`s constructed from a recording audio
    stream.
    Args:
        data_stream: A generator that yields raw audio data to send.
        rate: The sampling rate in hertz.
    """
    # The initial request must contain metadata about the stream, so the
    # server knows how to interpret it.
    recognition_config = cloud_speech.RecognitionConfig(
        # There are a bunch of config options you can specify. See
        # https://goo.gl/KPZn97 for the full list.
        encoding='LINEAR16',  # raw 16-bit signed LE samples
        sample_rate=rate,  # the rate in hertz
        # See
        # https://g.co/cloud/speech/docs/best-practices#language_support
        # for a list of supported languages.
        language_code='en-US',  # a BCP-47 language tag
    )
    streaming_config = cloud_speech.StreamingRecognitionConfig(
        config=recognition_config,
    )

    yield cloud_speech.StreamingRecognizeRequest(
        streaming_config=streaming_config)

    for data in data_stream:
        # Subsequent requests can all just have the content
        yield cloud_speech.StreamingRecognizeRequest(audio_content=data)


def listen_print_loop(recognize_stream):

    # game = np.array([[0,1,2,3],[0,0,0,2],[2,2,3,1],[1,0,0,3]])
    
    i = 0
    
    print (game)
    current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    print (current_time)
    cwd = os.getcwd()
    out_path = cwd+'/log/' + current_time + '/'

    out_file = cwd + 'game' + '.txt'
    # datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    if os.path.isfile('out_file.txt'):
        os.remove('out_file.txt')
        
    for resp in recognize_stream:


        temp_game = game

        if resp.error.code != code_pb2.OK:
            raise RuntimeError('Server error: ' + resp.error.message)

        # Display the transcriptions & their alternatives
        for result in resp.results:
            # print(result)
            # print (result.alternatives[0].transcript)
            if not(os.path.exists(out_path)):
	            os.makedirs(out_path)
            filename = out_path+'log_' + str(i) + '.txt'
            print(result.alternatives[0].transcript)
            log = open(filename, 'w')
            log.write(result.alternatives[0].transcript)
            log.close()
            # print(result.alternatives[0].transcript, file = log)
            i += 1

        
        if any(re.search(r'\b(pick)\b', alt.transcript, re.I)
               for result in resp.results
               for alt in result.alternatives):

            temp_game = game
            if any(re.search(r'\b(red)\b', alt.transcript, re.I)
               for result in resp.results
               for alt in result.alternatives):
                temp_game = game
                temp_game[temp_game != 1] = 0
                temp_game[temp_game == 1] = 1

                print (temp_game)

            if any(re.search(r'\b(green)\b', alt.transcript, re.I)
               for result in resp.results
               for alt in result.alternatives):
                temp_game = game
                temp_game[temp_game != 2] = 0
                temp_game[temp_game == 2] = 1
                print (temp_game)

            if any(re.search(r'\b(blue)\b', alt.transcript, re.I)
               for result in resp.results
               for alt in result.alternatives):
                temp_game = game
                temp_game[temp_game != 3] = 0
                temp_game[temp_game == 3] = 1

                print (temp_game)

            np.savetxt('out_file.txt', temp_game, fmt='%1d')
            


            


        # Exit recognition if any of the transcribed phrases could be
        # one of our keywords.
        if any(re.search(r'\b(finish|finished)\b', alt.transcript, re.I)
               for result in resp.results
               for alt in result.alternatives):

            err_game = np.array([[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1]])
            multi_commands = np.array([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])

            if not os.path.isfile('out_file.txt'):
                np.savetxt('out_file.txt', err_game, fmt='%1d')
                os.system('pkill -f streaming_linux.py')


            out_check = np.loadtxt('out_file.txt', dtype = 'int')
            current_game = np.loadtxt('game.txt', dtype = 'int')
            
            if np.array_equal(out_check, current_game) or np.array_equal(out_check, multi_commands):

                np.savetxt('out_file.txt', err_game, fmt='%1d')
            os.system('pkill -f streaming_linux.py')
            break


def main():
    with cloud_speech.beta_create_Speech_stub(
            make_channel('speech.googleapis.com', 443)) as service:
        # For streaming audio from the microphone, there are three threads.
        # First, a thread that collects audio data as it comes in
        with record_audio(RATE, CHUNK) as buffered_audio_data:
            # Second, a thread that sends requests with that data
            requests = request_stream(buffered_audio_data, RATE)
            # Third, a thread that listens for transcription responses
            recognize_stream = service.StreamingRecognize(
                requests, DEADLINE_SECS)

            # Exit things cleanly on interrupt
            signal.signal(signal.SIGINT, lambda *_: recognize_stream.cancel())

            # Now, put the transcription responses to use.
            try:
                listen_print_loop(recognize_stream)

                recognize_stream.cancel()
            except face.CancellationError:
                # This happens because of the interrupt handler
                pass


if __name__ == '__main__':
    main()