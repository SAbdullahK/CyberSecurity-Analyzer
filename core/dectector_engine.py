from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.decomposition import PCA

class IsolationForestDectector:
    def __init__(self, **kwargs):
        self.model = IsolationForest(n_estimators=50, contamination=0.05, **kwargs)

    def fit_predict(self, X):
        return self.model.fit_predict(X)
    
class LOFDectector:
    def __init__(self, **kwargs):
        self.model = LocalOutlierFactor(n_neighbors=10, **kwargs)

    def fit_predict(self, X):
        return self.model.fit_predict(X)
    
class PCADectector:
    def __init__(self, **kwargs):
        self.model = PCA(n_components=2, **kwargs)

    def fit_transform(self, X):
        return self.model.fit_transform(X)
    
    
    