import pandas as pd
import numpy as np

class StatsAnalyzer:
    def __init__(self, df, game_type='lotofacil'):
        self.df = df
        self.game_type = game_type
        self.total_numbers = 25 if game_type == 'lotofacil' else 60

    def calculate_frequencies(self):
        """Calculates global frequency of each number."""
        all_numbers = [n for sublist in self.df['numbers'] for n in sublist]
        counts = pd.Series(all_numbers).value_counts().sort_index()
        # Ensure all numbers 1..N are present even if 0 count
        for i in range(1, self.total_numbers + 1):
            if i not in counts:
                counts[i] = 0
        return counts.sort_values(ascending=False)

    def calculate_delays(self):
        """Calculates 'atraso' (delay) - how many draws since last appearance."""
        delays = {}
        last_draw_idx = self.df.index[-1]
        
        # We need to iterate backwards or keep track of last index
        # A simpler way:
        for num in range(1, self.total_numbers + 1):
            # Check appearances
            mask = self.df['numbers'].apply(lambda x: num in x)
            if not mask.any():
                delays[num] = len(self.df) # Never appeared
            else:
                last_appearance_idx = self.df[mask].index[-1]
                delays[num] = last_draw_idx - last_appearance_idx
        
        return pd.Series(delays).sort_values(ascending=False)
    
    def analyze_parity_distribution(self):
        """Returns the distribution of Even/Odd counts."""
        return self.df['pares'].value_counts().sort_index()

    def analyze_sum_distribution(self):
        """Returns stats about the sum."""
        return self.df['soma'].describe()
