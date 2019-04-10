from flask import Flask, request
import numpy as np
from keras.models import load_model

version='1.0'
app = Flask(__name__)

model = load_model('data/barzinga_model.h5')
model._make_predict_function()

@app.route("/", methods=['GET'])
def hello():
  return 'Welcome to the BarzingaML API! This is version %s' % version

@app.route("/predict", methods=['POST'])
def predict():
  img_rows, img_cols = 50, 150
  data = np.fromstring(request.data, dtype=int, sep=',')
  test = np.array([data])
  test = test.reshape(test.shape[0], img_rows, img_cols, 1)
  classes = model.predict_classes(test)
  return str(classes)

if __name__ == "__main__":
  app.run()
