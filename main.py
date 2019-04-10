from flask import Flask, request
import numpy as np
app = Flask(__name__)

from keras.models import load_model
model = load_model('data/barzinga_model.h5')
model._make_predict_function()

@app.route("/predict", methods=['POST'])
def predict():
  img_rows, img_cols = 50, 150
  data = np.fromstring(request.data, dtype=int, sep=',')
  test = np.array([data])
  test = test.reshape(test.shape[0], img_rows, img_cols, 1)
  print(test)
  classes = model.predict_classes(test)
  return str(classes)

if __name__ == "__main__":
  app.run()
