import random
from itertools import combinations
import pandas as pd

class Generator:
    def __init__(self, scorer):
        self.scorer = scorer
        self.scores = self.scorer.calculate_hybrid_score()
    
    def generate_candidate_pool(self, pool_size=18):
        """Selects the top N scoring numbers."""
        return self.scores.head(pool_size).index.tolist()

    def filter_games(self, games, config):
        """
        Filters a list of games based on config constraints.
        config: dict with 'min_sum', 'max_sum', 'min_odd', 'max_odd', etc.
        """
        valid_games = []
        for g in games:
            s = sum(g)
            odds = sum(1 for n in g if n % 2 != 0)
            
            if 'min_sum' in config and s < config['min_sum']: continue
            if 'max_sum' in config and s > config['max_sum']: continue
            if 'min_odd' in config and odds < config['min_odd']: continue
            if 'max_odd' in config and odds > config['max_odd']: continue
            
            valid_games.append(g)
        return valid_games
