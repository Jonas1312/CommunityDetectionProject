#!/usr/bin/env python
# coding:utf-8
"""
  Purpose:  Test different matrices for dense graphs
  Created:  04/03/2017
"""

import matplotlib.pyplot as plt
from stochasticBlockModel import SBM
from matrices import *
from sklearn.metrics.cluster import normalized_mutual_info_score
from spectralClustering import SpectralClustering

x = range(20, 1300, 200)
y_bethehessian = []
y_modularity = []
y_laplacian = []

n_communities = 2
cin = 0.6
cout = 0.4
probability_matrix = np.full((n_communities, n_communities), cout) + np.diag([cin - cout] * n_communities)

for i in x:  # dense graph
    n_vertices = i  # number of vertices
    sbm = SBM(n_vertices, n_communities, probability_matrix)

    spectral_labels, _, _, _ = SpectralClustering(n_communities, BetheHessian(sbm.adjacency_matrix), "BetheHessian")  # spectral clustering
    nmi = normalized_mutual_info_score(sbm.community_labels, spectral_labels)
    y_bethehessian.append(nmi)

    spectral_labels, _, _, _ = SpectralClustering(n_communities, ModularityMatrix(sbm.adjacency_matrix), "ModularityMatrix")  # spectral clustering
    nmi = normalized_mutual_info_score(sbm.community_labels, spectral_labels)
    y_modularity.append(nmi)

    spectral_labels, _, _, _ = SpectralClustering(n_communities, LaplacianMatrix(sbm.adjacency_matrix), "LaplacianMatrix") # spectral clustering
    nmi = normalized_mutual_info_score(sbm.community_labels, spectral_labels)
    y_laplacian.append(nmi)


plt.xlim(0, x[-1])
plt.title("Spectral clustering of a dense graph with several matrices")
plt.xlabel("Number of vertices")
plt.ylabel("Normalized Mutual Information Score")
plt.plot(x, y_bethehessian, 'r', label="Bethe-Hessian")
plt.plot(x, y_modularity, 'b', label="Modularity")
plt.plot(x, y_laplacian, 'g', label="Laplacian")
plt.legend(loc='upper right')
plt.show()
