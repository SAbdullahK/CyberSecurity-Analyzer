import pandas as pd
import numpy as np

class TrafficSimulator:
    def __init__(self, n_samples=100, anomaly_ratio=0.1, output="data/network.csv"):
        self.n_samples = n_samples
        self.anomaly_ratio = anomaly_ratio
        self.output = output

    def generate(self):
        normal_data = np.random.normal(0, 1, size=(int(self.n_samples*(1-self.anomaly_ratio)), 3))
        anomalies = np.random.normal(8, 2, size=(int(self.n_samples*self.anomaly_ratio), 3))
        data = np.vstack([normal_data, anomalies])
        np.random.shuffle(data)
        df = pd.DataFrame(data, columns= ["feature1","feature2","feature3"])
        df.to_csv(self.output, index=False)
        print(f"\n[SIM] Generate network traffic -> {self.output}")
        return df
        