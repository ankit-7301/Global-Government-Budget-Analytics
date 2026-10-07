import pandas as pd
from sqlalchemy import create_engine
import urllib.parse

def detect_budget_anomalies(country_name):
    host = "localhost"
    user = "root"
    password = "12345"
    database = "global_budget_db"
    password_quoted = urllib.parse.quote_plus(password)
    engine = create_engine(f"mysql+mysqlconnector://{user}:{password_quoted}@{host}/{database}")
    
    
    
    # Extract complete sequence for the country
    query = """
        SELECT b.year, b.total_budget_billions_usd
        FROM budgets b
        JOIN countries c ON b.country_id = c.country_id
        WHERE c.country_name = %s ORDER BY b.year ASC
    """
    df = pd.read_sql_query(query, engine, params=(country_name,))
    engine.dispose()
    
    if df.empty: return
    
    #Statistical Analysis Calculations
    mean_val = df['total_budget_billions_usd'].mean()
    std_val = df['total_budget_billions_usd'].std()
    
    #Calculate Rolling Z-Scores to flag shifts out of historical baselines
    df['z_score'] = (df['total_budget_billions_usd'] - mean_val) / std_val
    
    #Identity anomalies years where spending jumps outside a 95% confidence threshold (>1.96 standard deviations)
    anomalies = df[df['z_score'].abs() > 1.96]
    
    print(f"\n--- Flagged Fiscal Anomalies for {country_name} (Outlier Variance Analysis) ---")
    if anomalies.empty:
        print("No extreme statistical outliers identified.")
    else:
        print(anomalies)
    return anomalies

if __name__ == "__main__":
    detect_budget_anomalies("USA")