import pandas as pd
from core.data_loader import DataLoader
from core.features import FeatureExtractor
from analytics.stats import StatsAnalyzer
from prediction.scoring import Scorer
from prediction.generator import Generator
from desdobramento.engine import Unfolder

class BacktestSimulator:
    def __init__(self, df, game_type='lotofacil'):
        self.full_df = df
        self.game_type = game_type
        
    def run_simulation(self, start_idx, num_draws, pool_size=18, top_k_games=10):
        """
        Runs a simulation over a range of past draws.
        
        Args:
            start_idx: Index to start prediction tests (must have history before this).
            num_draws: How many consecutive draws to test.
            pool_size: How many numbers to pick from the scorer.
            top_k_games: How many final games to generate from the pool.
        """
        results = []
        
        end_idx = min(start_idx + num_draws, len(self.full_df))
        
        for i in range(start_idx, end_idx):
            # 1. Split Data
            # train_df includes everything UP TO i-1
            # target is 'numbers' at i
            train_df = self.full_df.iloc[:i].copy()
            target_draw = self.full_df.iloc[i]
            target_numbers = set(target_draw['numbers'])
            
            # 2. Pipeline
            # Stats -> Scorer -> Generator -> Unfolder
            stats = StatsAnalyzer(train_df, self.game_type)
            scorer = Scorer(stats)
            gen = Generator(scorer)
            
            # Get pool (e.g., predicted top 18 numbers)
            pool = gen.generate_candidate_pool(pool_size=pool_size)
            
            # Unfold this pool into games (simple full combos or top X)
            # For backtest speed, let's just create 'top_k_games' random fillings or simple unfolds
            # If pool_size is close to draw_size, Unfolder produces few games.
            # If large, it produces many. We strictly limit to top_k_games to simulate budget.
            unfolder = Unfolder(self.game_type)
            
            # If pool is big, full unfold is huge. We need a strategy.
            # Strategy: Generate 'top_k_games' from the pool.
            # For determinism in backtest, we might want just the first N combos, 
            # but usually we want "best fits". Our generator is simple, so we'll just take first valid ones.
            try:
                games = unfolder.unfold(pool, limit=top_k_games)
            except Exception as e:
                # Fallback if pool < draw_size (shouldn't happen with correct pool_size)
                games = []

            # 3. Evaluate
            best_acertos = 0
            total_acertos = 0
            
            for g in games:
                hits = len(target_numbers.intersection(set(g)))
                if hits > best_acertos:
                    best_acertos = hits
                total_acertos += hits
                
            avg_acertos = total_acertos / len(games) if games else 0
            
            results.append({
                'concurso': target_draw['concurso'] if 'concurso' in target_draw else i,
                'target': list(target_numbers),
                'pool': pool,
                'games_played': len(games),
                'best_hit': best_acertos,
                'avg_hit': avg_acertos
            })
            
        return pd.DataFrame(results)
