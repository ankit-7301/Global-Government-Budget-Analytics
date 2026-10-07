import pandas as pd
import os
import getpass
import mysql.connector
from mysql.connector import Error

def run_robust_etl(csv_path):
    
    df = pd.read_csv(csv_path)
    # handle any potetial global missing data issue
    df = df.fillna(0)
    
    host = os.environ.get("DB_HOST", "127.0.0.1")
    port = int(os.environ.get("DB_PORT", "3306"))
    user = os.environ.get("DB_USER", "root")
    password = os.environ.get("DB_PASSWORD", "12345")
    database = os.environ.get("DB_NAME", "global_budget_db")
    
    try:
        conn = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        cursor = conn.cursor()
        
        print("😁 Step 1:Seeding Country Dimension...")
        unique_countries = df['Country'].unique()
        for country in unique_countries:
            cursor.execute("INSERT IGNORE INTO countries (country_name) VALUES (%s)", (country.strip(),))
            
        # Explicitly commit the dimension table first
        conn.commit()
        
        #Build an in-memory dictionary to look up IDs instantly
        cursor.execute("SELECT country_name, country_id FROM countries")
        country_lookup = dict(cursor.fetchall())
        
        # The expected prefixes from the CSV columns (capitalized)
        sectors = ['Defence', 'Education', 'Health', 'Interest_Payments',
                   'Infrastructure', 'Agriculture', 'State_Transfers', 'Social_Welfare']
        
        print(f" Step 2: ingesting {len(df)} fact Records...")
        success_count = 0
        
        for idx, row in df.iterrows():
            try:
                country_name = str(row['Country']).strip()
                country_id = country_lookup.get(country_name)
                if country_id is None:
                    print(f" Warning: Country '{country_name}' not found in lookup — skipping row {idx}")
                    continue
                year = int(float(row['Year']))
                total_budget = float(row['Total_Budget_Billions_USD'])
                
                # Insert core budget header record (idempotent for reruns)
                cursor.execute(
                    "INSERT IGNORE INTO budgets (country_id, year, total_budget_billions_usd) VALUES (%s, %s, %s)",
                    (country_id, year, total_budget)
                )
                cursor.execute(
                    "SELECT budget_id FROM budgets WHERE country_id = %s AND year = %s LIMIT 1",
                    (country_id, year)
                )
                budget_row = cursor.fetchone()
                if budget_row is None:
                    raise RuntimeError(f"Unable to resolve budget_id for country_id={country_id}, year={year}")
                budget_id = budget_row[0]

                # Replace any previously imported sector rows for this budget so reruns stay consistent
                cursor.execute("DELETE FROM sector_allocations WHERE budget_id = %s", (budget_id,))
                
                # Unpivot and map indiviidual sector metrices
                for sector in sectors:
                    pct_col = f"{sector}_Percentage"
                    amt_col = f"{sector}_Amount_Billions_USD"
                    
                    allocated_pct = float(row[pct_col]) if pct_col in row.index and pd.notna(row[pct_col]) else 0.0
                    allocated_amt = float(row[amt_col]) if amt_col in row.index and pd.notna(row[amt_col]) else 0.0

                    cursor.execute(
                        """INSERT INTO sector_allocations
                            (budget_id, sector_name, allocation_percentage, allocation_amount_billions_usd)
                            VALUES (%s, %s, %s, %s)""",
                        (budget_id, sector, allocated_pct, allocated_amt)
                    )
                success_count += 1

            except Exception as row_err:
                print(f" Error processing row {idx} ({row.get('Country')} - {row.get('Year')}): {row_err}")
                continue
            
        # Critical: Final block save verification
        conn.commit()
        print(f" ETL Complete! Successfully Committed {success_count} structural record into MySql.")
        
    except Error as db_err:
        print(f" Structural database connection failure: {db_err}")
        print(f" Tried host={host}, port={port}, user={user}, database={database}")
    finally:
        if 'cursor' in locals() and cursor:
            try:
                cursor.close()
            except Exception:
                pass
        if 'conn' in locals() and conn and conn.is_connected():
            try:
                conn.close()
            except Exception:
                pass
        
if __name__== "__main__":

    run_robust_etl("Master_Global_Budgets_Historical.csv")
                    