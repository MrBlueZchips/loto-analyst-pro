import pandas as pd
import numpy as np
import datetime
import os

class DataLoader:
    def __init__(self, file_path=None, game_type='lotofacil'):
        """
        Initializes the DataLoader.
        
        Args:
            file_path (str): Path to the CSV/Excel file containing lottery data.
            game_type (str): 'lotofacil' or 'megasena'.
        """
        self.game_type = game_type
        
        if file_path:
             self.file_path = file_path
        else:
             # Auto-detect default files relative to this file's package root
             # This file is in core/data_loader.py -> parent is core -> parent is loto_analyst
             base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
             
             if game_type == 'lotofacil':
                 filename = "Lotofácil-resultados-30-12-2025.xlsx"
             else:
                 filename = "Mega-Sena_resultados-30-12-2025.xlsx"
            
             self.file_path = os.path.join(base_dir, filename)
                 
             if not os.path.exists(self.file_path):
                  print(f"Warning: Data file not found at {self.file_path}")

        self.df = None

    def load_data(self):
        """Loads data from CSV/Excel or generates mock data if no path found."""
        if self.file_path and os.path.exists(self.file_path):
            try:
                if self.file_path.endswith('.xlsx'):
                     self.df = pd.read_excel(self.file_path)
                else:
                     self.df = pd.read_csv(self.file_path)
                     
                self._normalize_columns()
            except Exception as e:
                print(f"Error loading file {self.file_path}: {e}")
                # Fallback to mock
                self.df = self._generate_mock_data()
        else:
            print(f"File not found: {self.file_path}. Using Mock Data.")
            self.df = self._generate_mock_data()
        
        self._post_process()
        return self.df

    def _normalize_columns(self):
        """Standardizes column names."""
        # Lowercase and strip
        self.df.columns = [str(c).lower().strip() for c in self.df.columns]
        
        # Map specific variations to standard names
        rename_map = {
            'data sorteio': 'data',
            'data do sorteio': 'data'
        }
        self.df.rename(columns=rename_map, inplace=True)

    def _generate_mock_data(self):
        """Generates realistic mock data for testing."""
        n_draws = 100
        if self.game_type == 'lotofacil':
            range_max = 25
            n_balls = 15
        else: # megasena
            range_max = 60
            n_balls = 6
        
        data = []
        start_date = datetime.date(2023, 1, 1)
        
        for i in range(1, n_draws + 1):
            numbers = sorted(np.random.choice(range(1, range_max + 1), n_balls, replace=False))
            row = {
                'concurso': i,
                'data': start_date + datetime.timedelta(days=i*2),
                'numbers': numbers # storing as list for easier processing internally
            }
            # Also add individual columns for compatibility
            for idx, n in enumerate(numbers):
                row[f'bola_{idx+1}'] = n
            data.append(row)
            
        return pd.DataFrame(data)

    def _post_process(self):
        """Ensures 'numbers' column exists as a list of integers."""
        # If we loaded from Excel, we likely have bola1, bola2... but NO 'numbers' column yet.
        if 'numbers' not in self.df.columns:
            # gather standard ball columns
            # usually: bola1, bola2... or bola 1, bola 2
            # Our normalization made them: bola1, bola2...
            ball_cols = [c for c in self.df.columns if c.startswith('bola') and c[4:].isdigit()]
            
            # Sort them just in case (bola1, bola10, bola2...)
            ball_cols.sort(key=lambda x: int(x[4:]))
            
            if ball_cols:
                self.df['numbers'] = self.df[ball_cols].values.tolist()
            else:
                # Fallback loose search
                ball_cols = [c for c in self.df.columns if 'bola' in c or 'dezen' in c]
                self.df['numbers'] = self.df[ball_cols].values.tolist()
        
        # Ensure numbers are integers and properly sorted/cleaned
        def clean_numbers(stats_list):
            # sometimes stats_list can contain NaNs or non-ints
            cleaned = []
            for x in stats_list:
                try:
                    cleaned.append(int(x))
                except:
                    pass
            return sorted(cleaned)

        self.df['numbers'] = self.df['numbers'].apply(clean_numbers)
        
        # Ensure Date
        if 'data' in self.df.columns:
            self.df['data'] = pd.to_datetime(self.df['data'], errors='coerce', dayfirst=True)
