CREATE DATABASE IF NOT EXISTS global_budget_db;
USE global_budget_db;



CREATE TABLE IF NOT EXISTS countries (
    country_id INT AUTO_INCREMENT PRIMARY KEY,
    country_name VARCHAR(100) UNIQUE NOT NULL
) ENGINE = InnoDB;


CREATE TABLE IF NOT EXISTS budgets (
    budget_id INT AUTO_INCREMENT PRIMARY KEY,
    country_id INT NOT NULL,
    year INT NOT NULL,
    total_budget_billions_usd DECIMAL(15,4) NOT NULL,

    FOREIGN KEY (country_id)
        REFERENCES countries(country_id)
        ON DELETE CASCADE,

    UNIQUE KEY uq_country_year (country_id, year),

    INDEX idx_year (year)

) ENGINE = InnoDB;



CREATE TABLE IF NOT EXISTS sector_allocations (
    allocation_id INT AUTO_INCREMENT PRIMARY KEY,
    budget_id INT NOT NULL,
    sector_name VARCHAR(100) NOT NULL,
    allocation_percentage DECIMAL(5,2) NOT NULL,
    allocation_amount_billions_usd DECIMAL(15,4) NOT NULL,

    FOREIGN KEY (budget_id)
        REFERENCES budgets(budget_id)
        ON DELETE CASCADE,

    INDEX idx_sector (sector_name)

) ENGINE = InnoDB;



SELECT * FROM countries;
SELECT * FROM budgets;
SELECT * FROM sector_allocations;



SELECT COUNT(*) AS Total_Countries
FROM countries;

SELECT COUNT(*) AS Total_Budgets
FROM budgets;

SELECT COUNT(*) AS Total_Sector_Allocations
FROM sector_allocations;


Show table status;
show create table sector_allocations;
show tables;

describe table  sector_allocations;
