import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def compare_america_mg():
    try:
        # Read the data
        print("Reading match data...")
        df = pd.read_csv('../DATA/team_performance_stats.csv', index_col=0)
        
        # Set América MG as the reference team
        america_mg = df.loc['América (MG)']
        
        # Create separate figures for each visualization
        # 1. Home vs Away Win Rate Comparison
        plt.figure(figsize=(12, 8))
        home_away_rates = df[['Home_Win_Rate', 'Away_Win_Rate']].sort_values('Home_Win_Rate', ascending=True)
        home_away_rates.plot(kind='barh')
        plt.title('Home vs Away Win Rates by Team', fontsize=14, pad=20)
        plt.xlabel('Win Rate (%)')
        plt.legend(['Home Win Rate', 'Away Win Rate'])
        
        # Highlight América MG
        america_idx = home_away_rates.index.get_loc('América (MG)')
        plt.axhline(y=america_idx, color='r', linestyle='--', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('../DATA/america_mg_win_rates.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 2. Away Goals Scored vs Conceded
        plt.figure(figsize=(12, 8))
        away_goals = pd.DataFrame({
            'Team': df.index,
            'Goals_Scored': df['Away_Goals_Scored'],
            'Goals_Conceded': df['Away_Goals_Conceded']
        }).sort_values('Goals_Scored', ascending=True)
        away_goals.plot(x='Team', kind='barh')
        plt.title('Away Goals Scored vs Conceded', fontsize=14, pad=20)
        plt.xlabel('Number of Goals')
        
        # Highlight América MG
        america_idx = away_goals.index.get_loc('América (MG)')
        plt.axhline(y=america_idx, color='r', linestyle='--', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('../DATA/america_mg_away_goals.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 3. Goal Difference
        plt.figure(figsize=(12, 8))
        goal_diff = df['Goal_Difference'].sort_values(ascending=True)
        goal_diff.plot(kind='barh')
        plt.title('Goal Difference by Team', fontsize=14, pad=20)
        plt.xlabel('Goal Difference')
        
        # Highlight América MG
        america_idx = goal_diff.index.get_loc('América (MG)')
        plt.axhline(y=america_idx, color='r', linestyle='--', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('../DATA/america_mg_goal_difference.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 4. Away Losses
        plt.figure(figsize=(12, 8))
        away_losses = df['Away_Losses'].sort_values(ascending=True)
        away_losses.plot(kind='barh')
        plt.title('Number of Away Losses by Team', fontsize=14, pad=20)
        plt.xlabel('Number of Losses')
        
        # Highlight América MG
        america_idx = away_losses.index.get_loc('América (MG)')
        plt.axhline(y=america_idx, color='r', linestyle='--', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('../DATA/america_mg_away_losses.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # Create comparison DataFrame
        league_avg = df.mean()
        comparison_data = {
            'Metric': [
                'Home Win Rate (%)',
                'Away Win Rate (%)',
                'Away Goals Scored',
                'Away Goals Conceded',
                'Goal Difference',
                'Away Losses'
            ],
            'América MG': [
                america_mg['Home_Win_Rate'],
                america_mg['Away_Win_Rate'],
                america_mg['Away_Goals_Scored'],
                america_mg['Away_Goals_Conceded'],
                america_mg['Goal_Difference'],
                america_mg['Away_Losses']
            ],
            'League Average': [
                league_avg['Home_Win_Rate'],
                league_avg['Away_Win_Rate'],
                league_avg['Away_Goals_Scored'],
                league_avg['Away_Goals_Conceded'],
                league_avg['Goal_Difference'],
                league_avg['Away_Losses']
            ],
            'Difference': [
                america_mg['Home_Win_Rate'] - league_avg['Home_Win_Rate'],
                america_mg['Away_Win_Rate'] - league_avg['Away_Win_Rate'],
                america_mg['Away_Goals_Scored'] - league_avg['Away_Goals_Scored'],
                america_mg['Away_Goals_Conceded'] - league_avg['Away_Goals_Conceded'],
                america_mg['Goal_Difference'] - league_avg['Goal_Difference'],
                america_mg['Away_Losses'] - league_avg['Away_Losses']
            ]
        }
        
        comparison_df = pd.DataFrame(comparison_data)
        
        # Save comparison to CSV
        comparison_df.to_csv('../DATA/america_mg_comparison.csv', index=False)
        
        # Print detailed comparison
        print("\nAmérica MG Comparison with League Average")
        print("=" * 80)
        print("\nDetailed comparison saved to america_mg_comparison.csv")
        print("\nVisualizations saved as separate files:")
        print("- america_mg_win_rates.png")
        print("- america_mg_away_goals.png")
        print("- america_mg_goal_difference.png")
        print("- america_mg_away_losses.png")
        
        print("\nKey Statistics:")
        print(comparison_df.to_string(index=False))
        
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    compare_america_mg() 