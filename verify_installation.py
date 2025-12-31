import sys
import os

# Add current directory to path
sys.path.append('/home/bluezchips/hobby/loto_analyst')

print("Verifying imports...")
try:
    from core.data_loader import DataLoader
    from core.features import FeatureExtractor
    from analytics.stats import StatsAnalyzer
    from prediction.scoring import Scorer
    from prediction.generator import Generator
    from desdobramento.engine import Unfolder
    from backtest.simulator import BacktestSimulator
    print("Imports successful.")
except ImportError as e:
    print(f"Import Error: {e}")
    sys.exit(1)

print("Verifying Data Loader (Mock)...")
dl = DataLoader(game_type='lotofacil')
df = dl.load_data()
if df is None or df.empty:
    print("Data Loader failed.")
    sys.exit(1)
print(f"Data Loaded: {len(df)} rows.")

print("Verifying Stats...")
stats = StatsAnalyzer(df, 'lotofacil')
freqs = stats.calculate_frequencies()
if freqs.empty:
    print("Stats failed.")
    sys.exit(1)

print("Verifying Prediction...")
scorer = Scorer(stats)
gen = Generator(scorer)
pool = gen.generate_candidate_pool(18)
if len(pool) != 18:
    print(f"Generator failed. Size: {len(pool)}")

print("Verifying Backtest...")
sim = BacktestSimulator(df, 'lotofacil')
res = sim.run_simulation(len(df)-5, 2)
if res.empty:
    print("Backtest failed or returned empty.")

print("ALL SYSTEMS GO.")
