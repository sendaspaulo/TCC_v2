import pandas as pd
from datetime import datetime

def add_coach_info():
    # Read the data
    df = pd.read_csv('../DATA/GPS_with_matches.csv')
    
    # Convert DATA column to datetime
    df['DATA'] = pd.to_datetime(df['DATA'])
    
    # Define coach periods
    coach_periods = [
        {
            'coach': 'Givanildo Oliveira',
            'start': '2018-11-11',
            'end': '2019-05-01'
        },
        {
            'coach': 'Adilson Batista',
            'start': '2018-07-24',
            'end': '2018-11-10'
        },
        {
            'coach': 'Ricardo Drubscky',
            'start': '2018-06-20',
            'end': '2018-07-23'
        },
        {
            'coach': 'Enderson Moreira',
            'start': '2016-07-20',
            'end': '2018-06-19'
        }
    ]
    
    # Add coach column
    df['Coach'] = None
    
    # Assign coach based on date ranges
    for period in coach_periods:
        mask = (df['DATA'] >= pd.to_datetime(period['start'])) & (df['DATA'] <= pd.to_datetime(period['end']))
        df.loc[mask, 'Coach'] = period['coach']
    
    # Save the modified dataframe
    print("Saving updated data to GPS_with_matches.csv...")
    df.to_csv('../DATA/GPS_with_matches.csv', index=False)
    
    # Print summary of coach assignments
    print("\nCoach Assignment Summary:")
    print("=" * 50)
    for period in coach_periods:
        count = len(df[df['Coach'] == period['coach']])
        print(f"{period['coach']}: {count} records")
    
    print("\nData update completed successfully!")

if __name__ == "__main__":
    add_coach_info() 