import pandas as pd

def calculate_metrics(results_df, game_type='lotofacil'):
    """Summarizes backtest results."""
    if results_df.empty:
        return {}
    
    summary = {
        'Simulações Totais': len(results_df),
        'Média de Acertos': results_df['best_hit'].mean(),
        'Máximo Acerto': results_df['best_hit'].max(),
        'Contagem de Acertos': results_df['best_hit'].value_counts().to_dict()
    }
    
    # Calculate specific prize tiers
    if game_type == 'lotofacil':
        summary['15_acertos'] = len(results_df[results_df['best_hit'] == 15])
        summary['14_acertos'] = len(results_df[results_df['best_hit'] == 14])
        summary['13_acertos'] = len(results_df[results_df['best_hit'] == 13])
    elif game_type == 'megasena':
        summary['Sena (6)'] = len(results_df[results_df['best_hit'] == 6])
        summary['Quina (5)'] = len(results_df[results_df['best_hit'] == 5])
        summary['Quadra (4)'] = len(results_df[results_df['best_hit'] == 4])
        
    return summary
