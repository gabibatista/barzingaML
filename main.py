from flask import Flask, request, Response
import numpy as np
from keras.models import load_model
import json

version='1.1'

app = Flask(__name__)

model = load_model('data/barzinga_model.h5')
model._make_predict_function()
productsDictFile = open("data/products_dict.json", "r")
productsDict = json.loads(productsDictFile.read())

@app.route("/", methods=['GET'])
def hello():
  return 'Welcome to the BarzingaML API! This is version %s' % version

@app.route("/predict", methods=['POST'])
def predict():
  img_rows, img_cols = 50, 150
  data = np.fromstring(request.data, dtype=int, sep=',')
  test = np.array([data])

  a = []
  for i in range(0, 2500):
      a.append(.2126)
      a.append(.7152)
      a.append(.0722)
  a = np.array(a)

  test = (test / 255) * a

  test = test.reshape(test.shape[0], img_rows, img_cols, 1)
  label = model.predict_classes(test)[0]
  items = list(filter(lambda product: product["label"] == label, productsDict))
  if len(items) > 0:
    return items[0]["id"]

  return Response("Server error", status=500)

if __name__ == "__main__":
  app.run()
