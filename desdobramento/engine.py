from itertools import combinations
import random

class Unfolder:
    def __init__(self, game_type='lotofacil'):
        self.game_type_config = {
            'lotofacil': {'draw_size': 15, 'max_num': 25},
            'megasena': {'draw_size': 6, 'max_num': 60}
        }
        self.config = self.game_type_config.get(game_type, self.game_type_config['lotofacil'])

    def unfold(self, selected_numbers, fixed_numbers=None, limit=None, override_draw_size=None):
        """
        Generates full games from the selected numbers.
        
        Args:
            selected_numbers (list): The pool of numbers to generate games from.
            fixed_numbers (list): Numbers that must appear in every game.
            limit (int): Max number of games to generate.
            override_draw_size (int): Optional size to override standard game size.
        """
        draw_size = override_draw_size if override_draw_size else self.config['draw_size']
        fixed = set(fixed_numbers) if fixed_numbers else set()
        variable = [n for n in selected_numbers if n not in fixed]
        
        needed = draw_size - len(fixed)
        
        if needed < 0:
            raise ValueError("Too many fixed numbers for the game type.")
        if len(variable) < needed:
            raise ValueError("Not enough numbers to complete the game.")
            
        # Generate combinations
        combs = combinations(variable, needed)
        
        games = []
        for c in combs:
            full_game = sorted(list(fixed) + list(c))
            games.append(full_game)
            if limit and len(games) >= limit:
                break
                
        return games
    
    def random_fill(self, fixed_numbers, n_games=1):
        """Fills the rest of the game randomly."""
        draw_size = self.config['draw_size']
        max_num = self.config['max_num']
        fixed = set(fixed_numbers) if fixed_numbers else set()
        
        games = []
        for _ in range(n_games):
            needed = draw_size - len(fixed)
            possible = [x for x in range(1, max_num + 1) if x not in fixed]
            chosen = random.sample(possible, needed)
            games.append(sorted(list(fixed) + chosen))
            
        return games
