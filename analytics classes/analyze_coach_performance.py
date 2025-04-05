import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def analyze_coach_performance():
    try:
        # Read the data
        print("Reading data...")
        df = pd.read_csv('../DATA/GPS_with_matches.csv')
        
        # Filter only match days (where Local is not empty)
        match_data = df[df['Local'].notna()].drop_duplicates(subset=['DATA'])
        
        # Calculate metrics for each coach
        coach_metrics = {}
        
        for coach in match_data['Coach'].unique():
            coach_games = match_data[match_data['Coach'] == coach]
            
            metrics = {
                'Total Games': len(coach_games),
                'Win Rate (%)': (coach_games['GP'] > coach_games['GC']).mean() * 100,
                'Goals Scored (avg)': coach_games['GP'].mean(),
                'Goals Conceded (avg)': coach_games['GC'].mean(),
                'Ball Possession (avg)': coach_games['Posse'].mean(),
                'Home Win Rate (%)': (coach_games[coach_games['Local'] == 'Em casa']['GP'] > 
                                    coach_games[coach_games['Local'] == 'Em casa']['GC']).mean() * 100,
                'Away Win Rate (%)': (coach_games[coach_games['Local'] == 'Visitante']['GP'] > 
                                    coach_games[coach_games['Local'] == 'Visitante']['GC']).mean() * 100
            }
            coach_metrics[coach] = metrics
        
        # Print results
        print("\nPerformance Analysis by Coach")
        print("=" * 80)
        for coach, metrics in coach_metrics.items():
            print(f"\nCoach: {coach}")
            print("-" * 40)
            for metric, value in metrics.items():
                print(f"{metric}: {value:.2f}")
        
        # Create visualizations
        plt.figure(figsize=(15, 12))
        
        # 1. Win Rate Comparison
        plt.subplot(2, 2, 1)
        win_rates = pd.DataFrame({
            'Coach': list(coach_metrics.keys()),
            'Win Rate (%)': [metrics['Win Rate (%)'] for metrics in coach_metrics.values()]
        })
        sns.barplot(data=win_rates, x='Coach', y='Win Rate (%)')
        plt.xticks(rotation=45)
        plt.title('Overall Win Rate by Coach')
        
        # 2. Goals Scored and Conceded
        plt.subplot(2, 2, 2)
        goals_data = []
        for coach, metrics in coach_metrics.items():
            goals_data.extend([
                {'Coach': coach, 'Goals': metrics['Goals Scored (avg)'], 'Type': 'Scored'},
                {'Coach': coach, 'Goals': metrics['Goals Conceded (avg)'], 'Type': 'Conceded'}
            ])
        goals_df = pd.DataFrame(goals_data)
        sns.barplot(data=goals_df, x='Coach', y='Goals', hue='Type')
        plt.xticks(rotation=45)
        plt.title('Average Goals Scored and Conceded by Coach')
        
        # 3. Home vs Away Win Rates
        plt.subplot(2, 2, 3)
        location_data = []
        for coach, metrics in coach_metrics.items():
            location_data.extend([
                {'Coach': coach, 'Win Rate (%)': metrics['Home Win Rate (%)'], 'Location': 'Home'},
                {'Coach': coach, 'Win Rate (%)': metrics['Away Win Rate (%)'], 'Location': 'Away'}
            ])
        location_df = pd.DataFrame(location_data)
        sns.barplot(data=location_df, x='Coach', y='Win Rate (%)', hue='Location')
        plt.xticks(rotation=45)
        plt.title('Home vs Away Win Rates by Coach')
        
        # 4. Ball Possession
        plt.subplot(2, 2, 4)
        possession_data = pd.DataFrame({
            'Coach': list(coach_metrics.keys()),
            'Ball Possession (%)': [metrics['Ball Possession (avg)'] for metrics in coach_metrics.values()]
        })
        sns.barplot(data=possession_data, x='Coach', y='Ball Possession (%)')
        plt.xticks(rotation=45)
        plt.title('Average Ball Possession by Coach')
        
        plt.tight_layout()
        plt.savefig('../DATA/coach_performance_analysis.png')
        plt.close()
        
        print("\nAnalysis completed successfully! Check DATA/coach_performance_analysis.png for visualizations.")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    analyze_coach_performance() 