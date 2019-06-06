# # Classificação de Imagens - Barzinga
from sklearn.preprocessing import StandardScaler
from time import time
import pandas as pd
import numpy as np


# ## Carregando Dados
np.random.seed(100)
df = pd.read_csv('data/dataset.csv', header=None)

df.loc[df[7500] == 'oreo', 7500] = 0
df.loc[df[7500] == 'sensacao', 7500] = 1
df.loc[df[7500] == 'duo', 7500] = 2
df.loc[df[7500] == 'trident', 7500] = 2


# ## Split de Dados
df_train = df.iloc[:900, :]
df_test = df.iloc[900:, :]


# ## Features
a = []
for i in range(0, 2500):
    a.append(.2126)
    a.append(.7152)
    a.append(.0722)

a = np.array(a)

X_train = (df_train.iloc[:, :-1].values / 255) * a
X_test = (df_test.iloc[:, :-1].values / 255) * a

# ## Dados
y_train = df_train[7500].values
y_train_onehot = pd.get_dummies(df_train[7500]).values
y_test = df_test[7500].values


# ## Rede Neural Convolucional
from keras import initializers
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout, Conv2D, MaxPooling2D, Flatten

start = time()

img_rows, img_cols = 50, 150
nb_filters = 16
pool_size = (2, 2)
kernel_size = (4, 4)

X_train = X_train.reshape(X_train.shape[0], img_rows, img_cols, 1)
X_test = X_test.reshape(X_test.shape[0], img_rows, img_cols, 1)
input_shape = (img_rows, img_cols, 1)

model = Sequential()

model.add(Conv2D(nb_filters, kernel_size, input_shape=input_shape, kernel_initializer=initializers.random_normal(stddev=0.01)))

model.add(Activation('relu'))

model.add(Conv2D(nb_filters, kernel_size))

model.add(Activation('relu'))

model.add(Conv2D(nb_filters, kernel_size))

model.add(Activation('relu'))

model.add(Conv2D(nb_filters, kernel_size))

model.add(Activation('relu'))

model.add(Conv2D(nb_filters, kernel_size))

model.add(Activation('relu'))

model.add(MaxPooling2D(pool_size = pool_size))

model.add(Dropout(0.25))

model.add(Flatten())

model.add(Dense(200))

model.add(Activation('relu'))

model.add(Dropout(0.3))

model.add(Dense(3))

model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adadelta', metrics=['accuracy'])

model.fit(X_train, y_train_onehot, epochs=8)

print ('\nTempo gasto: %s segundos' % str(time() - start))


y_prediction = model.predict_classes(X_test)
print ("\nAcurácia", np.sum(y_prediction == y_test) / float(len(y_test)))

from keras.models import load_model
model.save('data/barzinga_model.h5')
