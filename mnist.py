# -*- coding: utf-8 -*-
"""week 7 training

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NouZ7nHRpKYGKFkFohdUbt4uMtopd4b0
"""

import numpy as np
import pandas as pd
import sklearn
import sklearn.model_selection

def sigmoid(x: int) -> float:
  """Sigmoid activation function."""
  return 1 / (1 + np.exp(-x))

def sigmoid_back(x: int) -> float:
  """Derivative of sigmoid for backward calculation."""
  fwd = sigmoid(x)
  return fwd * (1-fwd)

class MLP:
  """A Neural Network Class to Perform Basic Feedforward algorithm and training"""
  def __init__(self, sizes: list):
    """Initialize a numpy array or a list of weights an array or list of weights depending on sizes"""
    self.sizes = sizes
    self.num_layers = len(sizes)
    self.weights = []
    self.biases = []

    self.__init_params()
    return

  def __init_params(self):
    """Initialize random weights and biases based on size parameters."""
    for i in range(1, self.num_layers):
        # X inputs -> Y Ouputs
        in_size = self.sizes[i-1]
        out_size = self.sizes[i]

        # weights.shape = (Y, X), biases.shape = (Y, 1)
        # e.g. 2 -> 3: weights is (2, 3), biases is (1, 3)
        self.weights.append(np.random.randn(out_size, in_size) * 0.1)
        self.biases.append(np.random.randn(out_size, 1) * 0.1)

  def forward(self, x: np.ndarray):
    """
      Perform feedforward algorithm on input vector for all layers

      Input:    x: np.ndarray with shape (1, self.sizes[0])

      Returns:  y: np.ndarray with shape (1, self.sizes[-1])
    """

    # Store inner layers for backward calculation (?)
    x = x.reshape(x.shape[0], 1)
    activations = [x]
    zs = []

    for i in range(self.num_layers-1):
      x = np.matmul(self.weights[i], x) + self.biases[i]
      zs.append(x)
      x = sigmoid(x)
      activations.append(x)

    return x, activations, zs

  def backward(self, x: np.ndarray, y: np.ndarray):

    """Return a tuple ``(delta_w, delta_b)`` representing the
        gradient for the cost function C_x.  ``nabla_b`` and
        ``nabla_w`` are layer-by-layer lists of numpy arrays, similar
        to ``self.biases`` and ``self.weights``."""
    delta_b = [np.zeros(b.shape) for b in self.biases]
    delta_w = [np.zeros(w.shape) for w in self.weights]
    # feedforward
    activation = x
    res, activations, zs = self.forward(activation)
    # backward pass
    delta = (activations[-1] - y) * sigmoid_back(zs[-1])
    delta_b[-1] = delta
    delta_w[-1] = np.dot(delta, activations[-2].transpose())

    for l in range(2, self.num_layers):
        z = zs[-l]
        sp = sigmoid_back(z)
        delta = np.dot(self.weights[-l+1].transpose(), delta) * sp
        delta_b[-l] = delta
        delta_w[-l] = np.dot(delta, activations[-l-1].transpose())
    return (delta_w, delta_b)

  def train(self, X_train, y_train, epochs=1, lr=0.01, batch_size=1, verbose=True):
      """Using forward and backward functions, fit the model on an entire training step using gradient descent algorithm."""
      k = 0
      n = X_train.shape[0]
      d_x = X_train.shape[1]
      d_y = y_train.shape[1]

      prev_loss = self.calc_squared_loss(X_train, y_train)
      new_loss = prev_loss
      while (k < 1e6 and (k == 0 or abs(prev_loss - new_loss) > 1e-5)):
        for x, y in zip(X_train, y_train):
          x = x.reshape((d_x, 1))
          y = y.reshape((d_y, 1))
          y = one_hot(y)
          delta_w, delta_b = self.backward(x, y)
          for i in range(len(self.weights)):
            self.weights[i] -= lr * delta_w[i]
            self.biases[i] -= lr * delta_b[i]

          prev_loss = new_loss
          new_loss = self.calc_squared_loss(X_train, y_train)

          if verbose:
            print(f"Iteration {k}, mean squared loss: {new_loss}")
          k+=1

  def sgd_train(self, X_train, y_train, epochs=1, lr=0.01, batch_size=1, verbose=True):
    """Using forward and backward functions, fit the model on an entire training step using gradient descent algorithm."""
    e = 0
    k = 0
    n = X_train.shape[0]
    d_x = X_train.shape[1]
    d_y = y_train.shape[1]

    while (e < epochs):
      rng = np.random.permutation(X_train.shape[0])
      for i in range(batch_size):
        x = X_train[rng[i]].reshape((d_x, 1))
        y = y_train[rng[i]].reshape((d_y, 1))
        l = one_hot(y)
        delta_w, delta_b = self.backward(x, l)
        for i in range(len(self.weights)):
          self.weights[i] -= lr * delta_w[i]
          self.biases[i] -= lr * delta_b[i]
        k+=1

    #   if verbose:
    #     print(f"Epoch {e}, Iteration {k}, accuracy:")
      e+=1

  def calc_squared_loss(self, X, y):
    """Helper func to calculate squared loss given by 1/2(y-y')^2."""
    sum = 0
    n = X.shape[0]
    d = X.shape[1]
    for i in range(len(X)):
      y_v, _, _ = self.forward(X[i].reshape(d,1))
      sum += ((y[i] - y_v) ** 2) / 2
    return np.mean(sum)
  
  def evaluate(self, X_test, y_test):
    correct = 0
    n = X_test.shape[0]
    for x, y in zip(X_test, y_test):
      pred = self.forward(x)[0]
      if np.argmax(pred) == y[0]:
        correct += 1
    return correct / n
  

def one_hot(Y):
    MAX_VALUE = 10
    one_hot_Y = np.zeros((1, MAX_VALUE))
    one_hot_Y[np.arange(1), Y] = 1
    return one_hot_Y.T

def main():
    df = pd.read_csv('train.csv')
    inputs = np.array(df.iloc[:, 1:])
    np.divide(inputs, 256.0)
    labels = np.array(df.iloc[:, 0])  
    # nn = MLP([784, 700, 500, 300, 10])
    nn = MLP([784, 32, 32, 10])
    X = np.array(inputs)
    X = X / 256.0
    Y = np.array(labels)
    Y = Y.reshape((Y.shape[0], 1))
    X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(
    X,Y, random_state=104,test_size=0.5, shuffle=True)

    print(X.shape)
    print(Y.shape)
    nn.sgd_train(X_train, y_train, epochs=100, batch_size=2056, lr=0.15)

    # actually testing the data
    print(nn.sizes)
    print(nn.num_layers)
    print(f"Accuracy: {round(nn.evaluate(X_test, y_test) * 100, 2)}")
    with open("weights.txt", "w+") as f:
        f.write(f"Weights\n{len(nn.weights)}\n{nn.weights[0].shape}\n")
        for elem in nn.weights:
            np.savetxt(f, elem, delimiter=" ")
    with open("biases.txt", "w+") as f:
        f.write(f"Biases\n{len(nn.biases)}\n{nn.biases[0].shape}\n")
        for elem in nn.biases:
           np.savetxt(f, elem, delimiter=" ")


if __name__ == '__main__':
    main()

