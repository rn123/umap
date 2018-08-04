#!/usr/bin/env python

import numpy as np
from sklearn.datasets import fetch_mldata
from sklearn.model_selection import train_test_split
import umap
import matplotlib.pyplot as plt

mnist = fetch_mldata('MNIST original')
X_train, X_test, y_train, y_test = train_test_split(
    mnist.data,
    mnist.target,
    stratify=mnist.target,
    random_state=42
)

trans = umap.UMAP(s
    n_neighbors=10,
    random_state=42,
    input_metric='euclidean',
    output_metric='euclidean',
    init='spectral',
    verbose=True,
).fit(X_train)

corners = np.array([
    [ -6.2,  2.2], # 7
    [ -2.6,  8.1], # 4
    [ -7.0,-10.3], # 1
    [ 11.0,  4.5], # 0
])

test_pts = np.array([
    (corners[0]*(1-x) + corners[1]*x)*(1-y) +
    (corners[2]*(1-x) + corners[3]*x)*y
    for y in np.linspace(0, 1, 10)
    for x in np.linspace(0, 1, 10)
])

inv_trasnformed_points = trans.inverse_transform(test_pts)

plt.scatter(trans.embedding_[:, 0], trans.embedding_[:, 1], c=y_train, cmap='tab10')
plt.scatter(test_pts[:, 0], test_pts[:, 1], marker='x', c='k')

plt.figure()
fig, ax = plt.subplots(10, 10, squeeze=True)
for i in range(100):
    ax[i].imshow(inv_trasnformed_points[i].reshape(28, 28), origin='upper')
    ax[i].get_xaxis().set_visible(False)
    ax[i].get_yaxis().set_visible(False)

plt.show()
