# clean_gps.py
import pandas as pd

def clean_gps_data():
    try:
        # Read the CSV file
        print("Reading GPS_withMatchday.csv...")
        df = pd.read_csv('GPS_cleaned.csv')
        
        # Select only the specified columns
        columns_to_keep = [
            'Posicao',
            'ATLETA',
            'Presenca',
            'DATA',
            'EF',
            'Disttotalm',
            'Distaltaintensidadem',
            'MinutosTotais',
            'PSE',
            'PSEXMIN',
            'DES',
            'ACE',
            'Trimp',
            'days_until_match'
        ]
        
        print("Cleaning data...")
        # Create new dataframe with only the selected columns
        cleaned_df = df[columns_to_keep]
        
        # Fill blank values in days_until_match with 0
        cleaned_df['days_until_match'] = cleaned_df['days_until_match'].fillna(0)
        
        # Save the cleaned dataframe to a new CSV file
        print("Saving cleaned data to GPS_cleaned.csv...")
        cleaned_df.to_csv('GPS_cleaned.csv', index=False)
        
        print("Data cleaning completed successfully!")
        print(f"Number of rows processed: {len(cleaned_df)}")
        print(f"Number of columns in cleaned file: {len(columns_to_keep)}")
        
    except FileNotFoundError:
        print("Error: The file 'GPS_withMatchday.csv' was not found in the current directory.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    clean_gps_data()