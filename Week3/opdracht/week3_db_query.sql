-- dimensie tabellen
-- 1. dim_retailer
CREATE TABLE dim_retailer (
    RETAILER_CODE INT PRIMARY KEY, 
    COMPANY_NAME VARCHAR(100),
    RETAILER_NAME VARCHAR(100),
    ADDRESS_1 VARCHAR(255),
    ADDRESS_2 VARCHAR(255),
    CITY VARCHAR(100),
    REGION VARCHAR(100),
    COUNTRY_CODE INT,
    SEGMENT_NAME VARCHAR(100),  -- uit retailer_segment
    SEGMENT_DESCRIPTION VARCHAR(255),
    RETAILER_TYPE_EN VARCHAR(100), -- uit retailer_type
    CONTACT_FIRST_NAME VARCHAR(50), -- uit retailer_contact
    CONTACT_LAST_NAME VARCHAR(50), 
    CONTACT_E_MAIL VARCHAR(50),
    CONTACT_JOB_POSITION_EN VARCHAR(100),
    CONTACT_FAX VARCHAR(50),
    CONTACT_GENDER VARCHAR(20),
    CONTACT_EXTENSTION VARCHAR(20),
    RETAILER_STATUS VARCHAR(50) -- afleidende dimensie waarde
);


-- 2. dim_country
CREATE TABLE dim_country (
    COUNTRY_CODE INT PRIMARY KEY,
    NAME VARCHAR(100),
    LANGUAGE VARCHAR(50),
    IMAGE VARCHAR(255),
    CURRENCY VARCHAR(50),
    TERRITORY_NAME VARCHAR(100)
);


-- 3. dim_sales_branch
CREATE TABLE dim_sales_branch (
    SALES_BRANCH_CODE INT PRIMARY KEY,
    ADDRESS_1 VARCHAR(255),
    ADDRESS_2 VARCHAR(255),
    CITY VARCHAR(100),
    REGION VARCHAR(100),
    COUNTRY_CODE INT,
    CONSTRAINT FK_dim_sales_branch_country FOREIGN KEY (COUNTRY_CODE) REFERENCES dim_country(COUNTRY_CODE)
);


-- 4. dim_sales
CREATE TABLE dim_sales (
    SALES_STAFF_CODE INT PRIMARY KEY,
    FIRST_NAME VARCHAR(100),
    LAST_NAME VARCHAR(100),
    POSITION_EN VARCHAR(100),
    SALES_BRANCH_CODE INT, -- connectie met dim_branch
    WORK_PHONE VARCHAR(50),
    DATE_HIRED DATE,
    SALES_EXPERIENCE_LEVEL VARCHAR(50), -- afleidende dimensie waarde
    CONSTRAINT FK_dim_sales_branch FOREIGN KEY (SALES_BRANCH_CODE) REFERENCES dim_sales_branch(SALES_BRANCH_CODE)
);


-- 5. dim_product
CREATE TABLE dim_product (
    PRODUCT_NUMBER INT PRIMARY KEY,
    PRODUCT_NAME VARCHAR(100),
    DESCRIPTION VARCHAR(255),
    INTRODUCTION_DATE DATE,
    PRODUCTION_COST DECIMAL(10,2),
    MARGIN DECIMAL(10,2),
    PRODUCT_IMAGE VARCHAR(255),
    PRODUCTION_TYPE VARCHAR(100), -- uit product_type
    PRODUCT_LINE VARCHAR(100), -- uit product_line
    PRODUCT_CATEGORY VARCHAR(100) -- afleidende dimensie waarde
);


-- 6. dim_time
CREATE TABLE dim_time (
    DATE INT PRIMARY KEY,  
    YEAR INT,
    MONTH INT,
    DAY INT
);



-- feiten tabellen

-- 1. fact_omzetten
CREATE TABLE fact_omzetten (
    ORDER_NUMBER INT,
    RETAILER_SITE_CODE INT,      -- Koppeling naar dim_retailer (RETAILER_CODE)
    RETAILER_CONTACT_CODE INT,    
    SALES_STAFF_CODE INT,         -- Koppeling naar dim_sales (SALES_STAFF_CODE)
    SALES_BRANCH_CODE INT,        -- Koppeling naar dim_sales_branch (SALES_BRANCH_CODE)
    ORDER_DATE INT,               -- Koppeling naar dim_time (DATE)
    ORDER_METHOD_EN VARCHAR(100),        -- Koppeling naar dim_order_method (ORDER_METHOD_CODE)
    ORDER_DETAIL_CODE INT,
    PRODUCT_NUMBER INT,           -- Koppeling naar dim_product (PRODUCT_NUMBER)
    QUANTITY INT,
    UNIT_PRICE DECIMAL(10,2),
    UNIT_COST DECIMAL(10,2),
    UNIT_SALE_PRICE DECIMAL(10,2),
    TOTAL_REVENUE AS (QUANTITY * UNIT_SALE_PRICE) PERSISTED,  -- afleidende meetwaarde
    TOTAL_COST AS (QUANTITY * UNIT_COST) PERSISTED,  -- afleidende meetwaarde
    PROFIT AS (QUANTITY * UNIT_SALE_PRICE - QUANTITY * UNIT_COST) PERSISTED,  -- afleidende meetwaarde
    CONSTRAINT PK_fact_omzetten PRIMARY KEY (ORDER_NUMBER, PRODUCT_NUMBER),
    CONSTRAINT FK_fact_omzetten_time FOREIGN KEY (ORDER_DATE) REFERENCES dim_time(DATE),
    CONSTRAINT FK_fact_omzetten_retailer FOREIGN KEY (RETAILER_SITE_CODE) REFERENCES dim_retailer(RETAILER_CODE),
    CONSTRAINT FK_fact_omzetten_sales FOREIGN KEY (SALES_STAFF_CODE) REFERENCES dim_sales(SALES_STAFF_CODE),
    CONSTRAINT FK_fact_omzetten_sales_branch FOREIGN KEY (SALES_BRANCH_CODE) REFERENCES dim_sales_branch(SALES_BRANCH_CODE),
    CONSTRAINT FK_fact_omzetten_product FOREIGN KEY (PRODUCT_NUMBER) REFERENCES dim_product(PRODUCT_NUMBER)
);


-- 2. fact_trainingen
CREATE TABLE fact_trainingen (
    SALES_STAFF_CODE INT,       -- Koppeling naar dim_sales
    COURSE_DESCRIPTION VARCHAR(255),
    DATE INT,                   -- Koppeling naar dim_time (DATE)
    CONSTRAINT PK_fact_trainingen PRIMARY KEY (SALES_STAFF_CODE, DATE, COURSE_DESCRIPTION),
    CONSTRAINT FK_fact_trainingen_time FOREIGN KEY (DATE) REFERENCES dim_time(DATE),
    CONSTRAINT FK_fact_trainingen_sales FOREIGN KEY (SALES_STAFF_CODE) REFERENCES dim_sales(SALES_STAFF_CODE)
);


-- 3. fact_klant_tevredenheid
CREATE TABLE fact_klant_tevredenheid (
    DATE INT,                   -- Koppeling naar dim_time (DATE)
    SALES_STAFF_CODE INT,       -- Koppeling naar dim_sales (SALES_STAFF_CODE)
    SATISFACTION_TYPE VARCHAR(100),
    CONSTRAINT PK_fact_klant_tevredenheid PRIMARY KEY (DATE, SALES_STAFF_CODE, SATISFACTION_TYPE),
    CONSTRAINT FK_fact_klant_time FOREIGN KEY (DATE) REFERENCES dim_time(DATE),
    CONSTRAINT FK_fact_klant_sales FOREIGN KEY (SALES_STAFF_CODE) REFERENCES dim_sales(SALES_STAFF_CODE)
);


-- 4. fact_retouren
CREATE TABLE fact_retouren (
    RETURN_CODE INT PRIMARY KEY,
    RETURN_DATE INT,            -- Koppeling naar dim_time (DATE)
    ORDER_DETAIL INT,
    RETURN_REASON VARCHAR(100),
    RETURN_QUANTITY INT,
    PRODUCT_NUMBER INT,         -- Koppeling naar dim_product (PRODUCT_NUMBER)
    CONSTRAINT FK_fact_retouren_time FOREIGN KEY (RETURN_DATE) REFERENCES dim_time(DATE),
    CONSTRAINT FK_fact_retouren_product FOREIGN KEY (PRODUCT_NUMBER) REFERENCES dim_product(PRODUCT_NUMBER)
);


-- 5. fact_voorraadaantallen
CREATE TABLE fact_voorraadaantallen (
    DATE INT,                   -- Koppeling naar dim_time (DATE)
    PRODUCT_NUMBER INT,         -- Koppeling naar dim_product (PRODUCT_NUMBER)
    INVENTORY_COUNT INT,
    CONSTRAINT PK_fact_voorraadaantallen PRIMARY KEY (DATE, PRODUCT_NUMBER),
    CONSTRAINT FK_fact_voorraad_time FOREIGN KEY (DATE) REFERENCES dim_time(DATE),
    CONSTRAINT FK_fact_voorraad_product FOREIGN KEY (PRODUCT_NUMBER) REFERENCES dim_product(PRODUCT_NUMBER)
);


-- 6. fact_verkoopverwachtingen
CREATE TABLE fact_verkoopverwachtingen (
    PRODUCT_NUMBER INT,         -- Koppeling naar dim_product (PRODUCT_NUMBER)
    FORECAST_DATE INT,          -- Koppeling naar dim_time (DATE)
    EXPECTED_VOLUME INT,
    CONSTRAINT PK_fact_verkoopverwachtingen PRIMARY KEY (PRODUCT_NUMBER, FORECAST_DATE),
    CONSTRAINT FK_fact_forecast_time FOREIGN KEY (FORECAST_DATE) REFERENCES dim_time(DATE),
    CONSTRAINT FK_fact_forecast_product FOREIGN KEY (PRODUCT_NUMBER) REFERENCES dim_product(PRODUCT_NUMBER)
);

