import pandas as pd
from sqlalchemy import create_engine

def run_advanced_analytics():
    engine = create_engine(
        "mysql+mysqlconnector://root:12345@localhost/global_budget_db"
    )

    #1.Analysis: Year-over-Year (YoY) Growth & 5-year Rolling Moving Average
    moving_avg_query = """
        SELECT
            c.country_name, b.year, b.total_budget_billions_usd,
            AVG(b.total_budget_billions_usd) OVER (
                PARTITION BY c.country_name
                ORDER BY b.year
                ROWS BETWEEN 4 PRECEDING AND CURRENT ROW
            ) as rolling_5yr_avg
        FROM budgets b
        JOIN countries c ON b.country_id = c.country_id;
    """
    df_moving_avg = pd.read_sql_query(moving_avg_query, engine)
    print("---1. 5-Year Rolling Budget Trends ---\n", df_moving_avg.head())
    
    #2. Analysis: Historical Sector Dominance Matrix (Isolating the #1 funded sector per year)
    dominance_query = """ 
        WITH Rankedsectors AS (
            SELECT
                c.country_name, b.year, sa.sector_name, sa.allocation_percentage,
                DENSE_RANK() OVER (PARTITION BY c.country_name, b.year ORDER BY sa.allocation_percentage DESC) AS sector_rank
            FROM sector_allocations sa
            JOIN budgets b ON sa.budget_id = b.budget_id  
            JOIN countries c ON b.country_id = c.country_id
        )
        SELECT country_name, year, sector_name, allocation_percentage
        FROM Rankedsectors WHERE sector_rank = 1;
    """
    
    df_dom = pd.read_sql_query(dominance_query, engine)
    print("\n---2. Historical #1 Budget Priorities -I- \n", df_dom.head())

    engine.dispose()
    
if __name__ == "__main__":
    run_advanced_analytics()    