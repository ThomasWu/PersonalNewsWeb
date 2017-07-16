import news_classes
import numpy as np
import os
import pandas as pd
import pickle
import json
import pyjsonrpc
import sys
import tensorflow as tf
import time

from tensorflow.contrib.learn.python.learn.estimators import model_fn
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'classifier'))
import news_cnn_model

learn = tf.contrib.learn

SERVER_HOST = 'localhost'
SERVER_PORT = 6060

MODEL_DIR = '../model'
MODEL_UPDATE_LAG_IN_SECONDS = 60

N_CLASSES = 17

VARS_FILE = '../model/vars'
VOCAB_PROCESSOR_SAVE_FILE = '../model/vocab_processor_save_file'

n_words = 0

MAX_DOCUMENT_LENGTH = 500
vocab_processor = None

classifier = None

def restoreVars():
    with open(VARS_FILE, 'r') as f:
        global n_words
        n_words = pickle.load(f)
    global vocab_processor
    vocab_processor = learn.preprocessing.VocabularyProcessor.restore(VOCAB_PROCESSOR_SAVE_FILE)
    print vocab_processor
    print 'Vars updated.'

def loadModel():
    global classifier
    classifier = learn.Estimator(
        model_fn=news_cnn_model.generate_cnn_model(N_CLASSES, n_words),
        model_dir=MODEL_DIR
    )
    df = pd.read_csv('../training_data/labeled_news.csv', header=None)

    train_df = df[0:400]
    x_train = train_df[1]
    x_train = np.array(list(vocab_processor.transform(x_train)))
    y_train = train_df[0]
    classifier.evaluate(x_train, y_train)

restoreVars()
loadModel()

class ReloadModelHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        print "Model change detected"
        time.sleep(MODEL_UPDATE_LAG_IN_SECONDS)
        restoreVars()
        loadModel()


class RequestHandler(pyjsonrpc.HttpRequestHandler):
    @pyjsonrpc.rpcmethod
    def classify(self, text):
        text_series = pd.Series([text])
        predict_x = np.array(list(vocab_processor.transform(text_series)))
        y_predicted = [ p['class'] for p in classifier.predict(predict_x, as_iterable=True) ]
        topic = news_classes.class_map[str(y_predicted[0])]
        return topic


observer = Observer()
observer.schedule(ReloadModelHandler(), path=MODEL_DIR, recursive=False)
observer.start()

http_server = pyjsonrpc.ThreadingHttpServer(
    server_address=(SERVER_HOST, SERVER_PORT),
    RequestHandlerClass=RequestHandler
)

print 'Start predicting server on URL: %s:%d' % (SERVER_HOST, SERVER_PORT)

http_server.serve_forever()
