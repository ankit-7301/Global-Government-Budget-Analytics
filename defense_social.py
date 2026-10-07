import pandas as pd
from sqlalchemy import create_engine, text

def analyze_guns_vs_butter(selected_year: int = 2025):
    engine = create_engine("mysql+pymysql://root:12345@localhost/global_budget_db")

    query = text("""
    SELECT
        c.country_name,

        MAX(CASE
            WHEN sa.sector_name = 'Defense'
            THEN sa.allocation_percentage
        END) AS defense_pct,

        MAX(CASE
            WHEN sa.sector_name = 'Social Welfare'
            THEN sa.allocation_percentage
        END) AS social_pct,

        MAX(CASE
            WHEN sa.sector_name = 'Education'
            THEN sa.allocation_percentage
        END) AS education_pct,

        ROUND(
            (
                MAX(CASE
                    WHEN sa.sector_name = 'Social Welfare'
                    THEN sa.allocation_percentage
                END)
                +
                MAX(CASE
                    WHEN sa.sector_name = 'Education'
                    THEN sa.allocation_percentage
                END)
            )
            /
            NULLIF(
                MAX(CASE
                    WHEN sa.sector_name = 'Defense'
                    THEN sa.allocation_percentage
                END),
                0
            ),
            2
        ) AS civilian_to_defense_ratio

    FROM sector_allocations sa
    JOIN budgets b ON sa.budget_id = b.budget_id
    JOIN countries c ON b.country_id = c.country_id
    WHERE b.year = :selected_year
    GROUP BY c.country_name
    ORDER BY civilian_to_defense_ratio DESC;
    """)

    with engine.connect() as conn:
        df = pd.read_sql(query, conn, params={"selected_year": selected_year})

    if df.empty:
        print(f"No records found for year: {selected_year}")
        return None

    print(f"\n--- 🛡️ Guns vs. Butter Ratio Rankings ({selected_year}) ---")
    print(df.to_string(index=False))
    return df

# THIS LINE CALLS THE FUNCTION
if __name__ == "__main__":
    analyze_guns_vs_butter(2025)