import pandas as pd
import numpy as np

class Scorer:
    def __init__(self, stats_analyzer):
        self.stats = stats_analyzer
        self.frequencies = self.stats.calculate_frequencies()
        self.delays = self.stats.calculate_delays()
    
    def calculate_hybrid_score(self, w_freq=0.4, w_delay=0.4, w_trend=0.2):
        """
        Calculates a score for each number based on weights.
        Higher score = 'better' candidate according to the strategy.
        """
        # Normalize Frequency (0-1)
        max_freq = self.frequencies.max()
        norm_freq = self.frequencies / max_freq
        
        # Normalize Delay (0-1)
        # Note: Some strategies prefer high delay ("due to hit"), others low ("hot")
        # Here we assume high delay is good for "balance", but let's make it configurable in future
        max_delay = self.delays.max()
        norm_delay = self.delays / max_delay if max_delay > 0 else self.delays
        
        # Trend: This requires time-series slopes or recent windows.
        # For simplicity in this version, we equate Trend to 'Recent Freq' (last 10 draws)
        # We need access to the raw df for this, assuming stats_analyzer has it
        df = self.stats.df
        last_10 = df.tail(10)
        recent_counts = pd.Series([n for sublist in last_10['numbers'] for n in sublist]).value_counts()
        # fill missing
        for i in range(1, self.stats.total_numbers + 1):
             if i not in recent_counts: recent_counts[i] = 0
        
        max_recent = recent_counts.max()
        norm_recent = recent_counts / max_recent if max_recent > 0 else recent_counts
        
        scores = {}
        for n in range(1, self.stats.total_numbers + 1):
            s = (w_freq * norm_freq.get(n, 0)) + \
                (w_delay * norm_delay.get(n, 0)) + \
                (w_trend * norm_recent.get(n, 0))
            scores[n] = s
            
        return pd.Series(scores).sort_values(ascending=False)
