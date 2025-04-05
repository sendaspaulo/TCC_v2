import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

def analyze_team_performance():
    try:
        # Read the data
        print("Reading match data...")
        df = pd.read_csv('../DATA/allMatchs.csv')
        
        # Remove empty rows
        df = df.dropna(how='all')
        
        # Remove rows where Data is 'Data' (duplicate headers)
        df = df[df['Data'] != 'Data']
        
        # Convert date column to datetime
        df['Data'] = pd.to_datetime(df['Data'])
        
        # Extract goals from 'Resultado' column
        df[['Home_Goals', 'Away_Goals']] = df['Resultado'].str.extract(r'(\d+)–(\d+)')
        df[['Home_Goals', 'Away_Goals']] = df[['Home_Goals', 'Away_Goals']].astype(float)
        
        # Calculate basic statistics for each team
        teams = set(df['Em casa'].unique()) | set(df['Visitante'].unique())
        team_stats = {}
        
        for team in teams:
            # Home games
            home_games = df[df['Em casa'] == team]
            home_wins = len(home_games[home_games['Home_Goals'] > home_games['Away_Goals']])
            home_losses = len(home_games[home_games['Home_Goals'] < home_games['Away_Goals']])
            home_draws = len(home_games[home_games['Home_Goals'] == home_games['Away_Goals']])
            
            # Away games
            away_games = df[df['Visitante'] == team]
            away_wins = len(away_games[away_games['Away_Goals'] > away_games['Home_Goals']])
            away_losses = len(away_games[away_games['Away_Goals'] < away_games['Home_Goals']])
            away_draws = len(away_games[away_games['Away_Goals'] == away_games['Home_Goals']])
            
            # Calculate goals
            home_goals_scored = home_games['Home_Goals'].sum()
            home_goals_conceded = home_games['Away_Goals'].sum()
            away_goals_scored = away_games['Away_Goals'].sum()
            away_goals_conceded = away_games['Home_Goals'].sum()
            
            # Calculate streaks
            home_results = home_games.apply(lambda x: 'W' if x['Home_Goals'] > x['Away_Goals'] 
                                          else 'L' if x['Home_Goals'] < x['Away_Goals'] else 'D', axis=1).tolist()
            away_results = away_games.apply(lambda x: 'W' if x['Away_Goals'] > x['Home_Goals']
                                          else 'L' if x['Away_Goals'] < x['Home_Goals'] else 'D', axis=1).tolist()
            
            # Calculate longest win and loss streaks
            def get_longest_streak(results, streak_type):
                current_streak = 0
                max_streak = 0
                for result in results:
                    if result == streak_type:
                        current_streak += 1
                        max_streak = max(max_streak, current_streak)
                    else:
                        current_streak = 0
                return max_streak
            
            longest_win_streak = max(get_longest_streak(home_results, 'W'),
                                   get_longest_streak(away_results, 'W'))
            longest_loss_streak = max(get_longest_streak(home_results, 'L'),
                                    get_longest_streak(away_results, 'L'))
            
            team_stats[team] = {
                'Total_Games': len(home_games) + len(away_games),
                'Home_Wins': home_wins,
                'Home_Losses': home_losses,
                'Home_Draws': home_draws,
                'Away_Wins': away_wins,
                'Away_Losses': away_losses,
                'Away_Draws': away_draws,
                'Home_Goals_Scored': home_goals_scored,
                'Home_Goals_Conceded': home_goals_conceded,
                'Away_Goals_Scored': away_goals_scored,
                'Away_Goals_Conceded': away_goals_conceded,
                'Longest_Win_Streak': longest_win_streak,
                'Longest_Loss_Streak': longest_loss_streak
            }
        
        # Create DataFrame from team stats
        stats_df = pd.DataFrame.from_dict(team_stats, orient='index')
        
        # Calculate additional metrics
        stats_df['Win_Rate'] = ((stats_df['Home_Wins'] + stats_df['Away_Wins']) / stats_df['Total_Games'] * 100).round(2)
        stats_df['Home_Win_Rate'] = (stats_df['Home_Wins'] / (stats_df['Home_Wins'] + stats_df['Home_Losses'] + stats_df['Home_Draws']) * 100).round(2)
        stats_df['Away_Win_Rate'] = (stats_df['Away_Wins'] / (stats_df['Away_Wins'] + stats_df['Away_Losses'] + stats_df['Away_Draws']) * 100).round(2)
        stats_df['Goal_Difference'] = (stats_df['Home_Goals_Scored'] + stats_df['Away_Goals_Scored'] - 
                                     stats_df['Home_Goals_Conceded'] - stats_df['Away_Goals_Conceded'])
        
        # Create visualizations
        plt.figure(figsize=(20, 15))
        
        # 1. Win Rates Comparison
        plt.subplot(2, 2, 1)
        win_rates = stats_df[['Home_Win_Rate', 'Away_Win_Rate']].sort_values('Home_Win_Rate', ascending=True)
        win_rates.plot(kind='barh')
        plt.title('Home vs Away Win Rates by Team', fontsize=12, pad=20)
        plt.xlabel('Win Rate (%)')
        plt.legend(['Home Win Rate', 'Away Win Rate'])
        
        # 2. Goals Scored and Conceded
        plt.subplot(2, 2, 2)
        goals_data = pd.DataFrame({
            'Team': stats_df.index,
            'Goals_Scored': stats_df['Home_Goals_Scored'] + stats_df['Away_Goals_Scored'],
            'Goals_Conceded': stats_df['Home_Goals_Conceded'] + stats_df['Away_Goals_Conceded']
        }).sort_values('Goals_Scored', ascending=True)
        goals_data.plot(x='Team', kind='barh')
        plt.title('Total Goals Scored and Conceded by Team', fontsize=12, pad=20)
        plt.xlabel('Number of Goals')
        
        # 3. Longest Streaks
        plt.subplot(2, 2, 3)
        streaks = pd.DataFrame({
            'Team': stats_df.index,
            'Win_Streak': stats_df['Longest_Win_Streak'],
            'Loss_Streak': stats_df['Longest_Loss_Streak']
        }).sort_values('Win_Streak', ascending=True)
        streaks.plot(x='Team', kind='barh')
        plt.title('Longest Win and Loss Streaks by Team', fontsize=12, pad=20)
        plt.xlabel('Number of Games')
        
        # 4. Home vs Away Performance (Points)
        plt.subplot(2, 2, 4)
        home_away = pd.DataFrame({
            'Team': stats_df.index,
            'Home_Points': stats_df['Home_Wins'] * 3 + stats_df['Home_Draws'],
            'Away_Points': stats_df['Away_Wins'] * 3 + stats_df['Away_Draws']
        }).sort_values('Home_Points', ascending=True)
        home_away.plot(x='Team', kind='barh')
        plt.title('Points Earned at Home vs Away', fontsize=12, pad=20)
        plt.xlabel('Points')
        
        plt.tight_layout()
        plt.savefig('../DATA/team_performance_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # Print summary statistics
        print("\nTeam Performance Summary")
        print("=" * 80)
        print("\nTop 5 Teams by Overall Win Rate:")
        print(stats_df.nlargest(5, 'Win_Rate')[['Win_Rate', 'Home_Win_Rate', 'Away_Win_Rate']])
        
        print("\nTop 5 Teams by Goal Difference:")
        print(stats_df.nlargest(5, 'Goal_Difference')[['Goal_Difference', 'Home_Goals_Scored', 'Away_Goals_Scored']])
        
        print("\nLongest Win/Loss Streaks:")
        print(stats_df[['Longest_Win_Streak', 'Longest_Loss_Streak']].sort_values('Longest_Win_Streak', ascending=False).head())
        
        # Save detailed statistics to CSV
        stats_df.to_csv('../DATA/team_performance_stats.csv')
        print("\nDetailed statistics saved to team_performance_stats.csv")
        print("Visualizations saved to team_performance_analysis.png")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    analyze_team_performance() 