import numpy as np
from sklearn.decomposition import PCA


def pca(vectors, n_components=2):
    """
    Perform PCA on a given list of vectors.

    Parameters:
    vectors (list of list of floats): The input vectors.
    n_components (int): Number of principal components to keep.

    Returns:
    np.ndarray: Transformed vectors after PCA.
    """
    # Convert the list of vectors to a numpy array
    data = np.array(vectors)

    # Initialize PCA
    pca = PCA(n_components=n_components)

    # Fit and transform the data
    transformed_data = pca.fit_transform(data)

    return transformed_data
