from sklearn.decomposition import PCA
import numpy as np

# X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
X = np.array([[1, 0, 0, 1], [1, 1, 1, 0], [0, 1, 1, 1], [1, 0, 0, 0], [0, 0, 1, 1]])
pca = PCA(n_components=2)
newX = pca.fit_transform(X)
print(X)
print(newX)
print(pca.explained_variance_ratio_)
