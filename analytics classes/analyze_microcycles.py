import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def analyze_america_mg_microcycles():
    try:
        # Read the data
        print("Reading match data...")
        df = pd.read_csv('../DATA/allMatchs.csv')
        
        # Remove empty rows and duplicate headers
        df = df.dropna(how='all')
        df = df[df['Data'] != 'Data']
        
        # Convert date column to datetime
        df['Data'] = pd.to_datetime(df['Data'])
        
        # Filter for América MG matches (both home and away)
        america_mg = df[(df['Em casa'] == 'América (MG)') | (df['Visitante'] == 'América (MG)')].copy()
        america_mg = america_mg.sort_values('Data')
        
        # Calculate microcycles
        america_mg['Next_Match_Date'] = america_mg['Data'].shift(-1)
        america_mg['Microcycle'] = (america_mg['Next_Match_Date'] - america_mg['Data']).dt.days
        
        # Remove the last row (which will have NaN for microcycle)
        america_mg = america_mg.dropna(subset=['Microcycle'])
        
        # Remove World Cup break (36-day microcycle)
        america_mg = america_mg[america_mg['Microcycle'] < 10]
        
        # Extract goals and calculate results
        def extract_goals(result):
            try:
                # Handle different score formats
                if 'x' in result:
                    home, away = result.split('x')
                elif '–' in result:
                    home, away = result.split('–')
                else:
                    return 0, 0
                return float(home.strip()), float(away.strip())
            except:
                return 0, 0
        
        america_mg[['Home_Goals', 'Away_Goals']] = america_mg['Resultado'].apply(lambda x: pd.Series(extract_goals(x)))
        
        # Calculate match results for América MG
        america_mg['Is_Home'] = america_mg['Em casa'] == 'América (MG)'
        america_mg['Goals_For'] = america_mg.apply(lambda x: x['Home_Goals'] if x['Is_Home'] else x['Away_Goals'], axis=1)
        america_mg['Goals_Against'] = america_mg.apply(lambda x: x['Away_Goals'] if x['Is_Home'] else x['Home_Goals'], axis=1)
        america_mg['Result'] = america_mg.apply(lambda x: 'W' if x['Goals_For'] > x['Goals_Against'] else ('D' if x['Goals_For'] == x['Goals_Against'] else 'L'), axis=1)
        
        # Create microcycle analysis
        microcycle_stats = america_mg['Microcycle'].value_counts().sort_index()
        
        # Calculate performance metrics for each microcycle length
        performance_by_microcycle = []
        for microcycle in america_mg['Microcycle'].unique():
            matches = america_mg[america_mg['Microcycle'] == microcycle]
            total_matches = len(matches)
            wins = len(matches[matches['Result'] == 'W'])
            draws = len(matches[matches['Result'] == 'D'])
            losses = len(matches[matches['Result'] == 'L'])
            goals_for = matches['Goals_For'].sum()
            goals_against = matches['Goals_Against'].sum()
            
            performance_by_microcycle.append({
                'Microcycle': microcycle,
                'Total_Matches': total_matches,
                'Wins': wins,
                'Draws': draws,
                'Losses': losses,
                'Win_Rate': (wins / total_matches * 100) if total_matches > 0 else 0,
                'Points_Per_Match': ((wins * 3 + draws) / total_matches) if total_matches > 0 else 0,
                'Goals_For': goals_for,
                'Goals_Against': goals_against,
                'Goal_Difference': goals_for - goals_against,
                'Goals_For_Per_Match': goals_for / total_matches if total_matches > 0 else 0,
                'Goals_Against_Per_Match': goals_against / total_matches if total_matches > 0 else 0
            })
        
        performance_df = pd.DataFrame(performance_by_microcycle)
        performance_df = performance_df.sort_values('Microcycle')
        
        # Create visualizations
        plt.figure(figsize=(15, 10))
        
        # Win Rate by Microcycle
        plt.subplot(2, 2, 1)
        plt.bar(performance_df['Microcycle'], performance_df['Win_Rate'])
        plt.title('Win Rate by Microcycle Length')
        plt.xlabel('Days Between Matches')
        plt.ylabel('Win Rate (%)')
        plt.grid(True, alpha=0.3)
        
        # Points per Match by Microcycle
        plt.subplot(2, 2, 2)
        plt.bar(performance_df['Microcycle'], performance_df['Points_Per_Match'])
        plt.title('Points per Match by Microcycle Length')
        plt.xlabel('Days Between Matches')
        plt.ylabel('Points per Match')
        plt.grid(True, alpha=0.3)
        
        # Goals per Match by Microcycle
        plt.subplot(2, 2, 3)
        plt.bar(performance_df['Microcycle'], performance_df['Goals_For_Per_Match'], label='Goals For')
        plt.bar(performance_df['Microcycle'], -performance_df['Goals_Against_Per_Match'], label='Goals Against')
        plt.title('Goals per Match by Microcycle Length')
        plt.xlabel('Days Between Matches')
        plt.ylabel('Goals per Match')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Goal Difference by Microcycle
        plt.subplot(2, 2, 4)
        plt.bar(performance_df['Microcycle'], performance_df['Goal_Difference'])
        plt.title('Goal Difference by Microcycle Length')
        plt.xlabel('Days Between Matches')
        plt.ylabel('Goal Difference')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('../DATA/america_mg_microcycle_performance.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # Print analysis
        print("\nAmérica MG Performance Analysis by Microcycle (excluding World Cup break)")
        print("=" * 80)
        print("\nPerformance by Microcycle Length:")
        print(performance_df.to_string(index=False))
        
        # Save detailed analysis to CSV
        performance_df.to_csv('../DATA/america_mg_microcycle_performance.csv', index=False)
        
        # Print match schedule with results
        print("\nMatch Schedule with Results and Microcycles:")
        print("=" * 80)
        for _, row in america_mg.iterrows():
            opponent = row['Visitante'] if row['Em casa'] == 'América (MG)' else row['Em casa']
            home_away = "Home" if row['Em casa'] == 'América (MG)' else "Away"
            result = f"{row['Goals_For']}-{row['Goals_Against']} ({row['Result']})"
            print(f"Date: {row['Data'].strftime('%Y-%m-%d')} | {home_away} vs {opponent} | {result} | Microcycle: {row['Microcycle']} days")
        
        print("\nDetailed analysis saved to america_mg_microcycle_performance.csv")
        print("Visualization saved to america_mg_microcycle_performance.png")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    analyze_america_mg_microcycles() 