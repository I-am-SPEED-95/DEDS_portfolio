-- Dimensie: Retailer
CREATE TABLE dim_retailer (
    RETAILER_CODE INT PRIMARY KEY,       -- Uit 'retailer' of 'retailer_headquarters'       
    COMPANY_NAME VARCHAR(100),                   
    RETAILER_NAME VARCHAR(100),                  
    ADDRESS1 VARCHAR(255),
    ADDRESS2 VARCHAR(255),
    CITY VARCHAR(100),
    REGION VARCHAR(100),
    COUNTRY_CODE INT,                            
    SEGMENT_NAME VARCHAR(100),        -- Uit 'retailer_segment'           
    SEGMENT_DESCRIPTION VARCHAR(255),
    RETAILER_TYPE_EN VARCHAR(100),        -- Uit 'retailer_type'     
    RETAILER_STATUS VARCHAR(50),     -- Afgeleide dimensiewaarde 
    CONTACT_EMAIL VARCHAR(50),    -- Uit 'retailer_contact'
    CONTACT_FIRST_NAME VARCHAR(50),
    CONTACT_LAST_NAME VARCHAR(50)
);

-- Dimensie: Product
CREATE TABLE dim_product (
    PRODUCT_NUMBER INT PRIMARY KEY,              
    PRODUCT_NAME VARCHAR(100),              -- Uit 'product'     
    DESCRIPTION VARCHAR(255),
    INTRODUCTION_DATE DATE,
    PRODUCTION_COST DECIMAL(10,2),
    MARGIN DECIMAL(10,2),
    PRODUCT_IMAGE VARCHAR(255),
    PRODUCT_TYPE_EN VARCHAR(100),        -- Uit 'product_type'        
    PRODUCT_LINE_EN VARCHAR(100),        -- Uit 'product_line'         
    PRODUCT_CATEGORY VARCHAR(100)                -- Afgeleide dimensiewaarde 
);

-- Dimensie: Tijd
CREATE TABLE dim_time (
    DATE INT PRIMARY KEY,       
    MONTH INT,
    QUARTER INT,
    YEAR INT
);


-- Dimensie: Order Method
CREATE TABLE dim_order_method (
    ORDER_METHOD_CODE INT PRIMARY KEY,
    ORDER_METHOD_EN VARCHAR(100)
);


-- Dimensie: Sales
CREATE TABLE dim_sales (
    SALES_STAFF_CODE INT PRIMARY KEY,            
    FIRST_NAME VARCHAR(100),
    LAST_NAME VARCHAR(100),
    POSITION_EN VARCHAR(100),
    WORK_PHONE VARCHAR(50),
    DATE_HIRED DATE,
    SALES_BRANCH_CODE INT,          -- Koppeling aan de vestiging
    BRANCH_CITY VARCHAR(100),
    REGION VARCHAR(100),
    COUNTRY_CODE INT,               -- Land van de vestiging
    SALES_EXPERIENCE_LEVEL VARCHAR(50)  -- Afgeleide dimensiewaarde
);

-- Feitentabel: fact_orders (voor Omzetten)
CREATE TABLE fact_omzetten (
    ORDER_NUMBER INT,                            -- Order identificatie (uit order_header)
    RETAILER_SITE_CODE INT,                      -- Koppeling naar dim_retailer (gebruik RETAILER_CODE)
    RETAILER_CONTACT_CODE INT,                   
    SALES_STAFF_CODE INT,                        -- Koppeling naar dim_sales
    ORDER_DATE INT,                                    -- Koppeling naar dim_time (afgeleid van ORDER_DATE)
    ORDER_METHOD_CODE INT,                       -- Koppeling naar dim_order_method
    ORDER_DETAIL_CODE INT,
    PRODUCT_NUMBER INT,                          -- Koppeling naar dim_product
    QUANTITY INT,
    UNIT_PRICE DECIMAL(10,2),
    UNIT_COST DECIMAL(10,2),
    UNIT_SALE_PRICE DECIMAL(10,2),
    TOTAL_REVENUE AS (QUANTITY * UNIT_SALE_PRICE),  -- Afgeleide meetwaarde: Totale omzet
    TOTAL_COST AS (QUANTITY * UNIT_COST),           -- Afgeleide meetwaarde: Totale kosten
    PROFIT AS (QUANTITY * UNIT_SALE_PRICE - QUANTITY * UNIT_COST),  -- Afgeleide meetwaarde: Winst
    PRIMARY KEY (ORDER_NUMBER, PRODUCT_NUMBER),
    CONSTRAINT FK_FACT_RETAILER FOREIGN KEY (RETAILER_SITE_CODE) REFERENCES dim_retailer(RETAILER_CODE),
    CONSTRAINT FK_FACT_SALES FOREIGN KEY (SALES_STAFF_CODE) REFERENCES dim_sales(SALES_STAFF_CODE),
    CONSTRAINT FK_FACT_TIME FOREIGN KEY (ORDER_DATE) REFERENCES dim_time(DATE),
    CONSTRAINT FK_FACT_ORDERMETHOD FOREIGN KEY (ORDER_METHOD_CODE) REFERENCES dim_order_method(ORDER_METHOD_CODE),
    CONSTRAINT FK_FACT_PRODUCT FOREIGN KEY (PRODUCT_NUMBER) REFERENCES dim_product(PRODUCT_NUMBER)
);

-- Feitentabel: fact_voorraadaantallen
-- INVENTORY-tabel.

-- Een computed column DATE_KEY in formaat YYYYMMDD met de eerste dag van de maand. connectie met dim_tijd maken
CREATE TABLE fact_voorraadaantallen (
    INVENTORY_YEAR INT,        -- Jaar van de inventarisatie
    INVENTORY_MONTH INT,       -- Maand van de inventarisatie
    DATE_KEY AS (INVENTORY_YEAR * 10000 + INVENTORY_MONTH * 100 + 1) PERSISTED,  
    PRODUCT_NUMBER INT,        -- Koppeling naar dim_product
    INVENTORY_COUNT INT,       -- Voorraadaantal
    PRIMARY KEY (DATE_KEY, PRODUCT_NUMBER),
    CONSTRAINT FK_FV_PRODUCT FOREIGN KEY (PRODUCT_NUMBER) REFERENCES dim_product(PRODUCT_NUMBER),
    CONSTRAINT FK_FV_TIME FOREIGN KEY (DATE_KEY) REFERENCES dim_time(DATE)
);


-- Feitentabel: fact_verkoopverwachtingen
-- PRODUCT_FORECAST-tabel.
-- We nemen FORECAST_YEAR en FORECAST_MONTH en berekenen een DATE_KEY (eerste dag van de maand).
CREATE TABLE fact_verkoopverwachtingen (
    PRODUCT_NUMBER INT,         -- Koppeling naar dim_product
    FORECAST_YEAR INT,          -- Jaar van de forecast
    FORECAST_MONTH INT,         -- Maand van de forecast
    DATE_KEY AS (FORECAST_YEAR * 10000 + FORECAST_MONTH * 100 + 1) PERSISTED,  -- bv. 20230301
    EXPECTED_VOLUME INT,        -- Verwacht volume
    PRIMARY KEY (DATE_KEY, PRODUCT_NUMBER),
    CONSTRAINT FK_FV2_PRODUCT FOREIGN KEY (PRODUCT_NUMBER) REFERENCES dim_product(PRODUCT_NUMBER),
    CONSTRAINT FK_FV2_TIME FOREIGN KEY (DATE_KEY) REFERENCES dim_time(DATE)
);

