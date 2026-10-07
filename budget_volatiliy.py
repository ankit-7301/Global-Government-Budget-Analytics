from sqlalchemy import create_engine, text
import pandas as pd

def analyze_budget_volatility(country_name: str, window_years: int = 10):
    # Establish connection engine
    engine = create_engine("mysql+pymysql://root:12345@localhost/global_budget_db")

    # Secure parameter-bound SQL query using sqlalchemy.text
    query = text("""
        SELECT b.year, b.total_budget_billions_usd
        FROM budgets b
        JOIN countries c ON b.country_id = c.country_id
        WHERE c.country_name = :country_name 
        ORDER BY b.year ASC
    """)

    # Use a context manager to auto-close the connection
    with engine.connect() as conn:
        df = pd.read_sql(query, conn, params={"country_name": country_name})

    if df.empty:
        print(f"No records found for country: {country_name}")
        return None

    # Calculate Rolling Window Statistics
    # Set min_periods=3 if you want partial rolling results for shorter time series
    df['rolling_mean'] = df['total_budget_billions_usd'].rolling(window=window_years).mean()
    df['rolling_std'] = df['total_budget_billions_usd'].rolling(window=window_years).std()

    # Calculate Volatility Index (Coefficient of Variation %)
    df['volatility_index'] = (df['rolling_std'] / df['rolling_mean']) * 100

    # Display results
    clean_df = df.dropna().head(10)
    print(f"\n----- {window_years}-Year Volatility Index for {country_name} -----")
    print(clean_df.to_string(index=False))

    return df

if __name__ == "__main__":
    analyze_budget_volatility("USA")