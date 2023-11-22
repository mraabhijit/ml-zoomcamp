#!/usr/bin/env python
# coding: utf-8
# import tensorflow.lite as tflite

import tflite_runtime.interpreter as tflite
from keras_image_helper import create_preprocessor

preprocessor = create_preprocessor('xception', target_size=(299, 299))

interpreter = tflite.Interpreter(model_path='models/clothing-model.tflite')
interpreter.allocate_tensors()

input_index = interpreter.get_input_details()[0]['index']
output_index = interpreter.get_output_details()[0]['index']

classes = ['dress',
 'hat',
 'longsleeve',
 'outwear',
 'pants',
 'shirt',
 'shoes',
 'shorts',
 'skirt',
 't-shirt']

# url = 'http://bit.ly/mlbookcamp-pants'

def predict(url):

    X = preprocessor.from_url(url)

    interpreter.set_tensor(input_index, X)
    interpreter.invoke()

    preds_tflite = interpreter.get_tensor(output_index)

    float_preds = preds_tflite[0].tolist()

    return dict(zip(classes, float_preds))


def lambda_handler(event, context):
    url = event['url']
    result = predict(url)
    return result