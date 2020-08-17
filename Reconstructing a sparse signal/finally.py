# -*- coding: utf-8 -*-
"""Finally

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cQVJ1qb-XVkUufFOoczaze2Ie_Msb4lZ

# Importing
"""

# Commented out IPython magic to ensure Python compatibility.
# %tensorflow_version 2.x

import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import random

print(tf.__version__)

np.set_printoptions(threshold=np.inf) #For printing the whole matrix and not just a summery!

"""# Seeding"""

### Seeding the Randomness
np.random.seed(1300)
tf.random.set_seed(1300)

"""# Data Creation"""

### Initial Variables ###
Dim = 200 #Dimension of the sparse signal
Sparsity = 10 #Sparsity Level
##Signal Creation
N_training=100000
signal = np.zeros((N_training,Dim))  
for i in range(N_training):
  signal[i,np.random.permutation(Dim)[:Sparsity]]=1
  # signal[i,random.choices(range(Dim),k=Sparsity)]=1
counter = 0
#Sparsity Check
for i in range(N_training):
  if signal[i,:].sum()==10:
    counter=counter+1

#Normalization
# for i in range(N_training):
#   signal[i,:]=signal[i,:] / (signal[i,:].sum())

print('Normalized Signal Sample : {}'.format(signal[0,:]))

print(counter)  #Counting 10 sparsed signals

"""# Tensorflow Autoencoder (Functional)

### Autoencoder Network
"""

### Autoencoder ###
encoding_dim = 60 #encoder size

inputs = tf.keras.layers.Input(shape=(Dim,))   # 20 Dim vectors... 2 or 3 or 1000 vectors of the dimension 20

x = tf.keras.layers.Flatten()(inputs)

encoding = tf.keras.layers.Dense(encoding_dim, activation='linear', name='encoder')(x)

# middle = tf.keras.layers.Dense(0.5*encoding_dim ,activation='relu', name='middle_layer')(encoding)
# x = tf.keras.layers.Flatten()(encoding)

decoding = tf.keras.layers.Dense(70, activation='relu', name='decoder')(encoding)


Lay1 = tf.keras.layers.Dense(80, activation='relu')(decoding)
Lay1 = tf.keras.layers.Dense(90, activation='relu')(Lay1)
Lay2 = tf.keras.layers.Dense(100, activation='relu')(Lay1)
Lay3 = tf.keras.layers.Dense(100, activation='relu')(Lay2)
Lay4 = tf.keras.layers.Dense(100, activation='relu')(Lay3)
Lay5 = tf.keras.layers.Dense(100, activation='relu')(Lay4)
Lay6 = tf.keras.layers.Dense(100, activation='relu')(Lay5)
Lay7 = tf.keras.layers.Dense(Dim, activation='relu')(Lay6)
# Lay8 = tf.keras.layers.Dense(Dim, activation='relu')(Lay7)

autoencoder = tf.keras.models.Model(inputs=inputs, outputs=Lay7)

"""### The rest of the job"""

### Model Compiler ###
# Optimer = tf.keras.optimizers.SGD(learning_rate=0.001)
# OPTI = tf.keras.optimizers.RMSprop(learning_rate=0.001, rho=0.9)
autoencoder.compile(optimizer='adam',loss='mse')

autoencoder.fit(signal,signal,epochs=20,verbose=1)

"""### Testing the Autoencoder Network"""

inp = np.zeros((1,Dim))  
Indices = np.random.permutation(Dim)[:Sparsity]
inp[0,Indices]=0.1
print(inp.sum())

print(inp.shape)
print(signal[0,:].shape)

Encoder_Predictor = autoencoder.predict(inp)

print(inp.shape)
print(Encoder_Predictor.shape)

print(Indices)
# rec=np.array(np.where(np.abs(Encoder_Predictor)>1e-1))
Predictor_Sorted = -np.sort(-np.abs(Encoder_Predictor),axis=1)
Predictor_Indices = np.argsort(-np.abs(Encoder_Predictor),axis=1)
print(Predictor_Sorted[0,0])
print(Encoder_Predictor[0,Predictor_Indices[0,0]])
print(Predictor_Indices[0,0:int(len(Indices))])
# plt.plot(Encoder_Predictor.flatten())
# plt.plot(inp.flatten())

counter=0
for i in Predictor_Indices[0,0:int(len(Indices))]:
  if i in Indices:
    print('> equivalent value : {}\n'.format(i))
    counter = counter+1
print(counter)    # Counts how many indices are the same

plt.subplot(2,1,1)
plt.plot(inp[0,:])
plt.subplot(2,1,2)
plt.plot(Encoder_Predictor[0,:])
plt.show()
plt.figure
plt.plot(inp[0,:],'o')
plt.plot(Encoder_Predictor[0,:],'.')
plt.show()

