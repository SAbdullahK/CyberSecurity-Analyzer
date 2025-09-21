import pandas as pd
import random
from datetime import datetime, timedelta

class LogSimulator:
    def __init__(self, n_entries=50, output="data/logs.csv"):
        self.n_entries = n_entries
        self.output = output
        self.start_time = datetime.now()

    def generate(self):
        events = [
            "User login success",
            "User logout",
            "File accessed",
            "System idle",
            "Failed login attempt",
            "Unauthorized access detected",
            "Malware signature found",
        ]
        data = []
        for i in range(self.n_entries): 
            timestamp = self.start_time + timedelta(minutes=i)
            event = random .choice(events)
            data.append([timestamp.strftime("%Y-%m-%d %H:%M:%S"), event])
        df = pd.DataFrame(data, columns=["timestamp", "event"]) 
        df.to_csv(self.output, index = False)
        print(f"[SIM] Generated logs -> {self.output}")
        return df
    
        