import pandas as pd

def merge_gps_with_matches():
    try:
        # Read both CSV files
        print("Reading CSV files...")
        gps_df = pd.read_csv('GPS_cleaned.csv')
        matches_df = pd.read_csv('matches_clean.csv')
        
        # Convert date columns to datetime
        gps_df['DATA'] = pd.to_datetime(gps_df['DATA'])
        matches_df['Data'] = pd.to_datetime(matches_df['Data'])
        
        # Create new columns in GPS dataframe to store match information
        match_columns = ['Horário', 'Dia', 'Local', 'GP', 'GC', 'Oponente', 'Posse', 'Rodada']
        for col in match_columns:
            gps_df[col] = None
            
        # For each GPS entry, find matching match data
        print("Merging data...")
        for index, row in gps_df.iterrows():
            # Find match with the same date
            match_row = matches_df[matches_df['Data'] == row['DATA']]
            if not match_row.empty:
                # Fill match information
                for col in match_columns:
                    gps_df.at[index, col] = match_row.iloc[0][col]
        
        # Save the merged dataframe
        print("Saving merged data to GPS_with_matches.csv...")
        gps_df.to_csv('GPS_with_matches.csv', index=False)
        
        print("Data merging completed successfully!")
        print(f"Number of rows processed: {len(gps_df)}")
        print(f"Number of matches found: {len(matches_df)}")
        
    except FileNotFoundError:
        print("Error: One or both of the required CSV files were not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    merge_gps_with_matches()