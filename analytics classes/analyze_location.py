import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_home_away_performance():
    # Read the data
    df = pd.read_csv('../DATA/GPS_with_matches.csv')
    
    # Filter only match days (where Local is not empty)
    match_data = df[df['Local'].notna()].drop_duplicates(subset=['DATA'])
    
    # Calculate basic statistics for home and away games
    home_games = match_data[match_data['Local'] == 'Em casa']
    away_games = match_data[match_data['Local'] == 'Visitante']
    
    # Calculate performance metrics
    metrics = {
        'Total Games': len(match_data),
        'Home Games': len(home_games),
        'Away Games': len(away_games),
        'Home Win Rate': (home_games['GP'] > home_games['GC']).mean() * 100,
        'Away Win Rate': (away_games['GP'] > away_games['GC']).mean() * 100,
        'Home Goals Scored (avg)': home_games['GP'].mean(),
        'Away Goals Scored (avg)': away_games['GP'].mean(),
        'Home Goals Conceded (avg)': home_games['GC'].mean(),
        'Away Goals Conceded (avg)': away_games['GC'].mean(),
        'Home Ball Possession (avg)': home_games['Posse'].mean(),
        'Away Ball Possession (avg)': away_games['Posse'].mean()
    }
    
    # Print results
    print("\nPerformance Analysis - Home vs Away Games")
    print("=" * 50)
    for metric, value in metrics.items():
        print(f"{metric}: {value:.2f}")
    
    # Create visualizations
    plt.figure(figsize=(15, 10))
    
    # 1. Goals Scored and Conceded
    plt.subplot(2, 2, 1)
    goals_data = pd.DataFrame({
        'Location': ['Home', 'Away', 'Home', 'Away'],
        'Goals': [home_games['GP'].mean(), away_games['GP'].mean(),
                 home_games['GC'].mean(), away_games['GC'].mean()],
        'Type': ['Scored', 'Scored', 'Conceded', 'Conceded']
    })
    sns.barplot(data=goals_data, x='Location', y='Goals', hue='Type')
    plt.title('Average Goals Scored and Conceded')
    
    # 2. Win Rate
    plt.subplot(2, 2, 2)
    win_rate = pd.DataFrame({
        'Location': ['Home', 'Away'],
        'Win Rate (%)': [metrics['Home Win Rate'], metrics['Away Win Rate']]
    })
    sns.barplot(data=win_rate, x='Location', y='Win Rate (%)')
    plt.title('Win Rate by Location')
    
    # 3. Ball Possession
    plt.subplot(2, 2, 3)
    possession = pd.DataFrame({
        'Location': ['Home', 'Away'],
        'Ball Possession (%)': [metrics['Home Ball Possession (avg)'], 
                               metrics['Away Ball Possession (avg)']]
    })
    sns.barplot(data=possession, x='Location', y='Ball Possession (%)')
    plt.title('Average Ball Possession by Location')
    
    # 4. Goals Difference
    plt.subplot(2, 2, 4)
    goals_diff = pd.DataFrame({
        'Location': ['Home', 'Away'],
        'Goal Difference': [home_games['GP'].mean() - home_games['GC'].mean(),
                          away_games['GP'].mean() - away_games['GC'].mean()]
    })
    sns.barplot(data=goals_diff, x='Location', y='Goal Difference')
    plt.title('Average Goal Difference by Location')
    
    plt.tight_layout()
    plt.savefig('../DATA/home_away_analysis.png')
    plt.close()

if __name__ == "__main__":
    analyze_home_away_performance() 