import pandas as pd
from sqlalchemy import create_engine, text

def compute_sector_correlations(country_name: str):
    engine = create_engine("mysql+pymysql://root:12345@localhost/global_budget_db")

    # Secure query using sqlalchemy.text and named parameters
    query = text("""
        SELECT b.year, sa.sector_name, sa.allocation_percentage
        FROM sector_allocations sa
        JOIN budgets b ON sa.budget_id = b.budget_id
        JOIN countries c ON b.country_id = c.country_id
        WHERE c.country_name = :country_name
    """)

    # Open connection via context manager
    with engine.connect() as conn:
        df = pd.read_sql(query, conn, params={"country_name": country_name})

    if df.empty:
        print(f"No records found for country: {country_name}")
        return None

    # Pivot table from long format to wide format
    wide_df = df.pivot(
        index='year',
        columns='sector_name',
        values='allocation_percentage'
    ) 

    # Calculate Pearson Correlation Matrix
    correlation_matrix = wide_df.corr()

    print(f"\n--- Cross-Sector Correlation Matrix for {country_name} ---")
    print(correlation_matrix.round(2))

    return correlation_matrix

# This triggers execution when running the file directly
if __name__ == "__main__":
    compute_sector_correlations("USA")