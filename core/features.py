import pandas as pd
import numpy as np

def is_prime(n):
    if n <= 1: return False
    if n <= 3: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

PRIMES_LOTOFACIL = {n for n in range(1, 26) if is_prime(n)}
PRIMES_MEGASENA = {n for n in range(1, 61) if is_prime(n)}

class FeatureExtractor:
    def __init__(self, df, game_type='lotofacil'):
        self.df = df
        self.game_type = game_type
        self.primes = PRIMES_LOTOFACIL if game_type == 'lotofacil' else PRIMES_MEGASENA

    def extract_features(self):
        """Applies all feature transformations."""
        self.df['soma'] = self.df['numbers'].apply(sum)
        self.df['pares'] = self.df['numbers'].apply(lambda x: sum(1 for n in x if n % 2 == 0))
        self.df['impares'] = self.df['numbers'].apply(lambda x: len(x) - sum(1 for n in x if n % 2 == 0))
        self.df['primos'] = self.df['numbers'].apply(lambda x: sum(1 for n in x if n in self.primes))
        self.df['min'] = self.df['numbers'].apply(min)
        self.df['max'] = self.df['numbers'].apply(max)
        self.df['amplitude'] = self.df['max'] - self.df['min']
        
        # Repeating numbers from previous contest
        self.df['repetidos_ultimo'] = [0] * len(self.df)
        numbers_series = self.df['numbers'].tolist()
        
        repeats = [0] # First draw has 0 repeats
        for i in range(1, len(numbers_series)):
            prev = set(numbers_series[i-1])
            curr = set(numbers_series[i])
            repeats.append(len(curr.intersection(prev)))
        
        self.df['repetidos_ultimo'] = repeats
        
        return self.df
