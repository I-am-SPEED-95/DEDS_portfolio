#%% md
# # Werkcollege-opdrachten Week 1.3
#%% md
# ## Dependencies importeren
#%% md
# Kopieer in het codeblok hieronder van het vorige practicum de import-code voor de dependencies die het vaakst worden gebruikt om data in te lezen. Geef er ook de gebruikelijke aliassen aan.<br>
# Zet eventuele warnings uit.
#%%
import sqlite3
from pickle import HIGHEST_PROTOCOL
import numpy as np
import openpyxl
import pandas as pd
from datetime import date, datetime
import warnings

from openpyxl.styles.builtins import output
from pygments import highlight
from win32netcon import ACCESS_GROUP

warnings.simplefilter('ignore')
#%% md
# Zet het bestand go_sales_train.sqlite in een makkelijk te vinden map
#%% md
# ## Databasetabellen inlezen
#%% md
# Kopieer in het codeblok hieronder van het vorige practicum de code om een connectie met het bestand go_sales_train.sqlite te maken.
#%%
def makeConnection():
    con = sqlite3.connect("../project/data/raw/go_sales_train.sqlite")
    return con

def laadProduct(con):
    product = pd.read_sql_query("SELECT * FROM product", con)
    return product

def laadProductType(con):
    product_type = pd.read_sql_query("SELECT * FROM product_type", con)
    return product_type

def laadProductLine(con):
    product_line = pd.read_sql_query("SELECT * FROM product_line", con)
    return product_line

def laadSalesStaff(con):
    sales_staff = pd.read_sql_query("SELECT * FROM sales_staff", con)
    return sales_staff

def laadSalesBranch(con):
    sales_branch = pd.read_sql_query("SELECT * FROM sales_branch", con)
    return sales_branch

def laadRetailerSite(con):
    retailer_site = pd.read_sql_query("SELECT * FROM retailer_site", con)
    return retailer_site

def laadCountry(con):
    country = pd.read_sql_query("SELECT * FROM country", con)
    return country

def laadOrderHeader(con):
    order_header = pd.read_sql_query("SELECT * FROM order_header", con)
    return order_header

def laadOrderDetail(con):
    order_details = pd.read_sql_query("SELECT * FROM order_details", con)
    return order_details

def laadReturnedItems(con):
    returned_item = pd.read_sql_query("SELECT * FROM returned_item", con)
    return returned_item

def laadReturnedReasons(con):
    return_reason = pd.read_sql_query("SELECT * FROM return_reason", con)
    return return_reason
#%% md
# Lees van de ingelezen go_sales_train-database te volgende tabellen in met behulp van "SELECT * FROM *tabel*".
# - product
# - product_type
# - product_line
# - sales_staff
# - sales_branch
# - retailer_site
# - country
# - order_header
# - order_details
# - returned_item
# - return_reason
#%%
def loadTables(con):
    sql_query = "SELECT name FROM sqlite_master WHERE type='table';"
    return pd.read_sql(sql_query, con)

#%% md
# Krijg je een "no such table" error? Dan heb je misschien met .connect() per ongeluk een leeg  databasebestand (.sqlite) aangemaakt. <u>Let op:</u> lees eventueel de informatie uit het Notebook van werkcollege 1.1b nog eens goed door.
#%% md
# Als je tijdens onderstaande opdrachten uit het oog verliest welke tabellen er allemaal zijn, kan je deze Pythoncode uitvoeren:
#%%
#sql_query = "SELECT name FROM sqlite_master WHERE type='table';"
#Vul dit codeblok verder in
#Naam_tabellen = pd.read_sql(sql_query, con)
#Op de puntjes hoort de connectie naar go_sales_train óf go_staff_train óf go_crm_train te staan.
#print(Naam_tabellen)
#%% md
# erachter 
#%% md
# Let op! Voor alle onderstaande opdrachten mag je <u>alleen Python</u> gebruiken, <u>geen SQL!</u>
#%% md
# ## Selecties op één tabel zonder functies
#%% md
# Geef een overzicht met daarin de producten en hun productiekosten waarvan de productiekosten lager dan 100 dollar en hoger dan 50 dollar ligt. (2 kolommen, 23 rijen)
#%%
def vraag1(con):
    product = laadProduct(con)
    productiekosten_eisen = (product['PRODUCTION_COST'] > 50) & (product['PRODUCTION_COST'] < 100)
    result = product.loc[productiekosten_eisen, ("PRODUCT_NAME", "PRODUCTION_COST")]
    return result


#%% md
# Geef een overzicht met daarin de producten en hun marge waarvan de marge lager dan 20 % of hoger dan 60 % ligt. (2 kolommen, 7 rijen) 
#%%
def vraag2(con):
    product = laadProduct(con)
    marge_eisen = (product['MARGIN'] < 0.2) | (product['MARGIN'] > 0.6)
    return product.loc[marge_eisen, ["PRODUCT_NAME", "MARGIN"]]
#%% md
# Geef een overzicht met daarin de landen waar met francs wordt betaald. Sorteer de uitkomst op land.  (1 kolom, 3 rijen)
#%%
def vraag3(con):
    country = laadCountry(con)
    wordt_betaald_met_francs = country['CURRENCY_NAME'] == "francs"
    return country.loc[wordt_betaald_met_francs, ["COUNTRY"]].sort_values("COUNTRY")
#%% md
# Geef een overzicht met daarin de verschillende introductiedatums waarop producten met meer dan 50% marge worden geïntroduceerd (1 kolom, 7 rijen) 
#%%
def vraag4(con):
    product = laadProduct(con)
    meer_dan_50_marge = product['MARGIN'] > 0.5
    return product.loc[meer_dan_50_marge, "INTRODUCTION_DATE"].drop_duplicates()

#%% md
# Geef een overzicht met daarin het eerste adres en de stad van verkoopafdelingen waarvan zowel het tweede adres als de regio bekend is (2 kolommen, 7 rijen)
#%%
def vraag5(con):
    sales_branch = laadSalesBranch(con)
    not_null = (sales_branch['ADDRESS2'].notna()) & (sales_branch['REGION'].notna())
    return sales_branch.loc[not_null, ['ADDRESS1', 'CITY']]
#%% md
# Geef een overzicht met daarin de landen waar met dollars (dollars of new dollar) wordt betaald. Sorteer de uitkomst op land. (1 kolom, 4 rijen) 
#%%
def vraag6(con):
    country = laadCountry(con)
    landen_met_dollars = (country['CURRENCY_NAME'] == 'dollars') | (country['CURRENCY_NAME'] == 'new dollar')
    return country.loc[landen_met_dollars, ['COUNTRY']].sort_values(by='COUNTRY')
#%% md
# Geef een overzicht met daarin beide adressen en de stad van vestigingen van klanten waarvan de postcode begint met een ‘D’ (van duitsland). Filter op vestigingen die een tweede adres hebben. (3 kolommen, 2 rijen) 
#%%
def vraag7(con):
    retailer_site = laadRetailerSite(con)
    postcode_met_D = (retailer_site['POSTAL_ZONE'].str[0] == 'D') & (retailer_site['ADDRESS2'].notna())
    return retailer_site.loc[postcode_met_D, ['ADDRESS1', 'ADDRESS2', 'CITY']]
#%% md
# ## Selecties op één tabel met functies
#%% md
# Geef het totaal aantal producten dat is teruggebracht (1 waarde) 
#%%
def vraag8(con):
    returned_item = laadReturnedItems(con)
    return returned_item.loc[:, ['RETURN_QUANTITY']].sum()
#%% md
# Geef het aantal regio’s waarin verkoopafdelingen gevestigd zijn. (1 waarde)
#%%
def vraag9(con):
    sales_branch = laadSalesBranch(con)
    aantal_unieke_regios = sales_branch.loc[:, ['REGION']].drop_duplicates().shape[0]

    # Zet de integer in een DataFrame
    df = pd.DataFrame({'Aantal unieke regio\'s': [aantal_unieke_regios]})

    return df

#%% md
# Maak 3 variabelen:
# - Een met de laagste
# - Een met de hoogste
# - Een met de gemiddelde (afgerond op 2 decimalen)
# 
# marge van producten (3 kolommen, 1 rij) 
#%%
def vraag10(con):
    product = laadProduct(con)
    laagste = product['MARGIN'].min()
    hoogste = product['MARGIN'].max()
    gemiddelde = product['MARGIN'].mean()

    resultaat = pd.DataFrame({
        "Laagste": [laagste],
        "Hoogste": [hoogste],
        "Gemiddelde": [gemiddelde]
    })

    return resultaat
#%% md
# Geef het aantal vestigingen van klanten waarvan het 2e adres niet bekend is (1 waarde)
#%%
def vraag11(con):
    retailer_site = laadRetailerSite(con)
    address_not_known = retailer_site["ADDRESS2"].isna()
    aantal_onbekende_adressen = retailer_site.loc[address_not_known, :].shape[0]

    # Zet de integer in een DataFrame
    df = pd.DataFrame({'Aantal onbekende adressen': [aantal_onbekende_adressen]})

    return df

#%% md
# Geef de gemiddelde kostprijs van de verkochte producten waarop korting (unit_sale_price < unit_price) is verleend (1 waarde) 
#%%
def vraag12(con):
    order_details = laadOrderDetail(con)
    product = laadProduct(con)
    order_detail_product = pd.merge(order_details, product, left_on="PRODUCT_NUMBER", right_on="PRODUCT_NUMBER", how="inner")

    is_korting = order_detail_product["UNIT_SALE_PRICE"] < order_detail_product["UNIT_PRICE"]

    return order_detail_product.loc[is_korting, ["PRODUCTION_COST"]].mean()#%% md
# Geef een overzicht met daarin het aantal medewerkers per medewerkersfunctie (2 kolommen, 7 rijen) 
#%%
def vraag13(con):
    sales_staff = laadSalesStaff(con)
    return sales_staff.groupby("POSITION_EN").size()
#%% md
# 
#%% md
# Geef een overzicht met daarin per telefoonnummer het aantal medewerkers dat op dat telefoonnummer bereikbaar is. Toon alleen de telefoonnummer waarop meer dan 4 medewerkers bereikbaar zijn. (2 kolommen, 10 rijen) 
#%%
def vraag14(con):
    sales_staff = laadSalesStaff(con)
    sales_staff_2 = sales_staff["WORK_PHONE"].value_counts()
    resultaat = sales_staff_2[sales_staff_2 > 4]
    return resultaat
#%% md
# ## Selecties op meerdere tabellen zonder functies
#%% md
# Geef een overzicht met daarin het eerste adres en de stad van vestigingen van klanten uit ‘Netherlands’ (2 kolommen, 20 rijen) 
#%%
def vraag15(con):
    retailer_site = laadRetailerSite(con)
    country = laadCountry(con)
    retailer_site_country = pd.merge(retailer_site, country, left_on="COUNTRY_CODE", right_on="COUNTRY_CODE", how="inner")
    return retailer_site_country.loc[retailer_site_country["COUNTRY"] == "Netherlands", ['ADDRESS1', 'CITY']]
#%% md
# Geef een overzicht met daarin de productnamen die tot het producttype ‘Eyewear’ behoren. (1 kolom, 5 rijen) 
#%%
def vraag16(con):
    product = laadProduct(con)
    product_type = laadProductType(con)
    product_product_type = pd.merge(product, product_type, left_on="PRODUCT_TYPE_CODE", right_on="PRODUCT_TYPE_CODE", how="inner")
    return product_product_type.loc[product_product_type['PRODUCT_TYPE_EN'] == "Eyewear", ["PRODUCT_NAME"]]

#%% md
# Geef een overzicht met daarin alle unieke eerste adressen van klantvestigingen en de voornaam en achternaam van de verkopers die ‘Branch Manager’ zijn en aan deze vestigingen hebben verkocht (3 kolommen, 1 rij) 
#%%
def vraag17(con):
    retailer_site = laadRetailerSite(con)
    order_header = laadOrderHeader(con)
    sales_staff = laadSalesStaff(con)
    retailer_site_order_header = pd.merge(retailer_site, order_header, left_on="RETAILER_SITE_CODE", right_on="RETAILER_SITE_CODE", how="inner")

    retailer_site_order_header_sales_staff = pd.merge(retailer_site_order_header, sales_staff, left_on="SALES_STAFF_CODE", right_on="SALES_STAFF_CODE", how="inner")

    return retailer_site_order_header_sales_staff.loc[retailer_site_order_header_sales_staff['POSITION_EN'] == "Branch Manager", ['FIRST_NAME', 'LAST_NAME' , 'ADDRESS1'] ].drop_duplicates()
#%% md
# Geef een overzicht met daarin van de verkopers hun functie en indien zij iets hebben verkocht de datum waarop de verkoop heeft plaatsgevonden. Laat alleen de verschillende namen van de posities zien van de verkopers die het woord ‘Manager’ in hun positienaam hebben staan. (2 kolommen, 7 rijen) 
#%%
def vraag18(con):
    order_header = laadOrderHeader(con)
    sales_staff = laadSalesStaff(con)

    retailer_site_order_header = pd.merge(order_header, sales_staff, left_on="SALES_STAFF_CODE", right_on="SALES_STAFF_CODE", how="right")

    has_manager_in_name = (retailer_site_order_header["POSITION_EN"].str.contains("Manager"))

    return retailer_site_order_header.loc[has_manager_in_name, ['POSITION_EN', 'ORDER_DATE'] ].drop_duplicates()

#%% md
# Geef een overzicht met daarin de verschillende namen van producten en bijbehorende namen van producttypen van de producten waarvoor ooit meer dan 750 stuks tegelijk verkocht zijn. (2 kolommen, 9 rijen) 
#%%
def vraag19(con):
    order_details = laadOrderDetail(con)
    product = laadProduct(con)
    product_type = laadProductType(con)

    retailer_site_product_data = pd.merge(order_details, product, left_on="PRODUCT_NUMBER", right_on="PRODUCT_NUMBER", how="inner")

    retailer_site_product_data = pd.merge(retailer_site_product_data, product_type, left_on="PRODUCT_TYPE_CODE", right_on="PRODUCT_TYPE_CODE", how="inner")

    has_more_than_750 = retailer_site_product_data['QUANTITY'] > 750

    retailer_site_product_data = retailer_site_product_data.loc[has_more_than_750, ['PRODUCT_NAME', 'PRODUCT_TYPE_EN']].drop_duplicates()

    return retailer_site_product_data
#%% md
# Geef een overzicht met daarin de productnamen waarvan ooit meer dan 40% korting is verleend. De formule voor korting is: (unit_price - unit_sale_price) / unit_price (1 kolom, 8 rijen) 
#%%
def vraag20(con):
    order_details = laadOrderDetail(con)
    product = laadProduct(con)
    retailer_site_product_data = pd.merge(order_details, product, left_on="PRODUCT_NUMBER", right_on="PRODUCT_NUMBER", how="inner")
    more_than_40_percent_discount = ((retailer_site_product_data['UNIT_PRICE'] - retailer_site_product_data['UNIT_SALE_PRICE']) / retailer_site_product_data['UNIT_PRICE']) > 0.4
    retailer_site_product_data = retailer_site_product_data.loc[more_than_40_percent_discount, ['PRODUCT_NAME']].drop_duplicates()
    return retailer_site_product_data
#%% md
# Geef een overzicht met daarin de retourreden van producten waarvan ooit meer dan 90% van de aangeschafte hoeveelheid is teruggebracht (return_quantity/quantity). (1 kolom, 3 rijen) 
#%%
def vraag21(con):
    order_details = laadOrderDetail(con)
    return_reason = laadReturnedReasons(con)
    returned_item = laadReturnedItems(con)

    returned_items_full_data = (
        returned_item
        .merge(order_details, on="ORDER_DETAIL_CODE")
        .merge(return_reason, on="RETURN_REASON_CODE")
    )

    return_percentage_filter = (returned_items_full_data['RETURN_QUANTITY'] / returned_items_full_data['QUANTITY']) > 0.9

    returned_items_filtered = (
        returned_items_full_data
        .loc[return_percentage_filter, ['RETURN_DESCRIPTION_EN']]
        .drop_duplicates()
    )

    return returned_items_filtered
#%% md
# ## Selecties op meerdere tabellen met functies
#%% md
# Geef een overzicht met daarin per producttype het aantal producten die tot dat producttype behoren. (2 kolommen, 21 rijen) 
#%%
def vraag22(con):
    product_type = laadProductType(con)
    product = laadProduct(con)

    producttypes = product_type.merge(product, on="PRODUCT_TYPE_CODE")

    # Groeperen op 'PRODUCT_TYPE_CODE' en het aantal producten tellen, inclusief de naam
    aantal_producten_per_type = (
        producttypes
        .groupby(["PRODUCT_TYPE_EN"])
        .size()
        .reset_index(name="Aantal Producten")
    )

    return aantal_producten_per_type
#%% md
# Geef een overzicht met daarin per land het aantal vestigingen van klanten die zich in dat land bevinden. (2 kolommen, 21 rijen) 
#%%
def vraag23(con):
    country = laadCountry(con)
    retailer_site = laadRetailerSite(con)
    landen_vestigingen = country.merge(retailer_site, on="COUNTRY_CODE")

    aantal_vestigingen_per_land = (
        landen_vestigingen
        .groupby(["COUNTRY"])
        .size()
        .reset_index(name="Aantal vestigingen")
    )

    return aantal_vestigingen_per_land
#%% md
# Geef een overzicht met daarin van de producten behorend tot het producttype ‘Cooking Gear’ per productnaam de totaal verkochte hoeveelheid en de gemiddelde verkoopprijs. Sorteer de uitkomst op totaal verkochte hoeveelheid. (4 kolommen, 10 rijen)
#%%
def vraag24(con):
    product_type = laadProductType(con)
    product = laadProduct(con)
    order_details = laadOrderDetail(con)
    producttypes = product_type.merge(product, on="PRODUCT_TYPE_CODE")
    producttypes_order_details = producttypes.merge(order_details, on="PRODUCT_NUMBER")

    is_cooking_gear = producttypes_order_details['PRODUCT_TYPE_EN'] == "Cooking Gear"
    cooking_gear = producttypes_order_details.loc[is_cooking_gear, :]

    summary = cooking_gear.groupby('PRODUCT_NAME').agg(
        Totaal_Verkocht=('QUANTITY', 'sum'),
        Gemiddelde_Prijs=('UNIT_SALE_PRICE', 'mean')
    ).reset_index()

    summary_sorted = summary.sort_values(by='Totaal_Verkocht', ascending=False)

    return summary_sorted
#%% md
# Geef een overzicht met daarin per land de naam van het land, de naam van de stad waar de verkoopafdeling is gevestigd (noem de kolomnaam in het overzicht ‘verkoper’) en het aantal steden waar zich klanten bevinden in dat land (noem de kolomnaam in het overzicht ‘klanten’) (3 kolommen, 29 rijen) 
#%%
def vraag25(con):
    country = laadCountry(con)
    sales_branch = laadSalesBranch(con)
    retailer_site = laadRetailerSite(con)

    country_branch = country.merge(sales_branch, on="COUNTRY_CODE").rename({'CITY': 'VERKOPER'}, axis=1)
    customer_count = country.merge(retailer_site, on="COUNTRY_CODE")

    summary = customer_count.groupby('COUNTRY').agg(
        aantal_klanten=('RETAILER_SITE_CODE', 'nunique')
    ).reset_index()

    resultaat = country_branch[['COUNTRY', 'VERKOPER']].drop_duplicates()

    final_result = pd.merge(resultaat, summary, on='COUNTRY', how='left')

    return final_result
#%% md
# ## Pythonvertalingen van SUBSELECT en UNION met o.a. for-loops
#%% md
# Geef een overzicht met daarin de voornaam en de achternaam van de medewerkers die nog nooit wat hebben verkocht (2 kolommen, 25 rijen) 
#%%
def vraag26(con):
    sales_staff = laadSalesStaff(con)
    order_header = laadOrderHeader(con)

    sales_staff_no_sold = sales_staff.merge(order_header, on="SALES_STAFF_CODE", how="left")

    has_not_sold_anything = sales_staff_no_sold['ORDER_NUMBER'].isna()

    return sales_staff_no_sold.loc[has_not_sold_anything, ["FIRST_NAME", "LAST_NAME"]]

#%% md
# Geef een overzicht met daarin het aantal producten waarvan de marge lager is dan de gemiddelde marge van alle producten samen. Geef in het overzicht tevens aan wat de gemiddelde marge is van dit aantal producten waarvan de marge lager dan de gemiddelde marge van alle producten samen is. (1 kolom, 2 rijen) 
#%%
def vraag27(con):
    product = laadProduct(con)

    gemiddelde_margin = product['MARGIN'].mean()
    lager_gemiddeld = product[product['MARGIN'] < gemiddelde_margin]
    aantal_lager_gemiddeld = lager_gemiddeld.shape[0]
    gemiddelde_margin_lager_gemiddeld = lager_gemiddeld['MARGIN'].mean()

    resultaat = pd.DataFrame({
        'Waarde': [aantal_lager_gemiddeld, gemiddelde_margin_lager_gemiddeld]
    }, index=['Aantal producten', 'Gemiddelde marge'])

    return resultaat
#%% md
# Geef een overzicht met daarin de namen van de producten die voor meer dan 500 (verkoopprijs) zijn verkocht maar nooit zijn teruggebracht. (1 kolom, 13 rijen) 
#%%
def vraag28(con):
    product = laadProduct(con)
    order_details = laadOrderDetail(con)
    returned_item = laadReturnedItems(con)

    producten_verkopen = product.merge(order_details, on="PRODUCT_NUMBER", how="inner")
    producten_verkopen_terug = producten_verkopen.merge(returned_item, on="ORDER_DETAIL_CODE", how="left")

    is_niet_teruggegeven = (producten_verkopen_terug['RETURN_CODE'].isna()) & (producten_verkopen_terug['UNIT_SALE_PRICE'] > 500)

    return producten_verkopen_terug.loc[is_niet_teruggegeven, ["PRODUCT_NAME"]].drop_duplicates()

#%% md
# Geef een overzicht met daarin per (achternaam van) medewerker of hij/zij manager is of niet, door deze informatie toe te voegen als extra 'Ja/Nee'-kolom.<br>
# Hint: gebruik een for-loop waarin je o.a. bepaalt of het woord 'Manager' in de functie (position_en) staat. (2 kolommen, 102 rijen).
#%%
def vraag29(con):
    sales_staff = laadSalesStaff(con)

    medewerkers_data = sales_staff.loc[:, ["LAST_NAME", "POSITION_EN"]]

    for index, medewerker in medewerkers_data.iterrows():
        rol = medewerkers_data.at[index, 'POSITION_EN']
        if "Manager" in rol:
            medewerkers_data.at[index, 'IS-MANAGER'] = "Ja"
        else:
            medewerkers_data.at[index, 'IS-MANAGER'] = "Nee"

    medewerkers_data = medewerkers_data.drop("POSITION_EN", axis=1)
    return medewerkers_data
#%% md
# Met de onderstaande code laat je Python het huidige jaar uitrekenen.
#%%
from datetime import date
date.today().year
#%% md
# Met de onderstaande code selecteer je op een bepaald jaartal uit een datum.
#%%
from datetime import datetime

date_str = '16-8-2013'
date_format = '%d-%m-%Y'
date_obj = datetime.strptime(date_str, date_format)

date_obj.year
#%% md
# Geef met behulp van bovenstaande hulpcode een overzicht met daarin op basis van het aantal jaar dat iemand in dienst is of een medewerker ‘kort in dienst’ (minder dan 25 jaar in dienst) of een ‘lang in dienst’ (groter gelijk dan 12 jaar in dienst) is. Geef daarbij per medewerker in een aparte kolom zowel ‘kort in dienst’ als ‘lang in dienst’ aan. Gebruik (wederom) een for-loop.<br>
# (2 kolommen, 102 rijen) 
#%%
def vraag30(con):
    sales_staff = laadSalesStaff(con)
    medewerkers_data = sales_staff.loc[:, ["LAST_NAME", "DATE_HIRED"]]

    huidig_jaar = date.today().year

    for index, medewerker in medewerkers_data.iterrows():
        date_hired = medewerkers_data.at[index, 'DATE_HIRED']
        date_str = date_hired
        date_format = '%Y-%m-%d'
        date_obj = datetime.strptime(date_str, date_format)
        aantal_jaar_in_dienst = huidig_jaar - date_obj.year

        if aantal_jaar_in_dienst < 25:
            medewerkers_data.at[index, 'DIENSTVERBAND'] = "Kort in dienst"
        else:
            medewerkers_data.at[index, 'DIENSTVERBAND'] = "Lang in dienst"

    medewerkers_data = medewerkers_data.drop("DATE_HIRED", axis=1)
    return medewerkers_data

#%% md
import os

output_dir = "../project/data/processed"
os.makedirs(output_dir, exist_ok=True)

con = makeConnection()

vraag1(con).to_excel(os.path.join(output_dir, "vraag1.xlsx"))
vraag2(con).to_excel(os.path.join(output_dir, "vraag2.xlsx"))
vraag3(con).to_excel(os.path.join(output_dir, "vraag3.xlsx"))
vraag4(con).to_excel(os.path.join(output_dir, "vraag4.xlsx"))
vraag5(con).to_excel(os.path.join(output_dir, "vraag5.xlsx"))
vraag6(con).to_excel(os.path.join(output_dir, "vraag6.xlsx"))
vraag7(con).to_excel(os.path.join(output_dir, "vraag7.xlsx"))
vraag8(con).to_excel(os.path.join(output_dir, "vraag8.xlsx"))
vraag9(con).to_excel(os.path.join(output_dir, "vraag9.xlsx"))
vraag10(con).to_excel(os.path.join(output_dir, "vraag10.xlsx"))
vraag11(con).to_excel(os.path.join(output_dir, "vraag11.xlsx"))
vraag12(con).to_excel(os.path.join(output_dir, "vraag12.xlsx"))
vraag13(con).to_excel(os.path.join(output_dir, "vraag13.xlsx"))
vraag14(con).to_excel(os.path.join(output_dir, "vraag14.xlsx"))
vraag15(con).to_excel(os.path.join(output_dir, "vraag15.xlsx"))
vraag16(con).to_excel(os.path.join(output_dir, "vraag16.xlsx"))
vraag17(con).to_excel(os.path.join(output_dir, "vraag17.xlsx"))
vraag18(con).to_excel(os.path.join(output_dir, "vraag18.xlsx"))
vraag19(con).to_excel(os.path.join(output_dir, "vraag19.xlsx"))
vraag20(con).to_excel(os.path.join(output_dir, "vraag20.xlsx"))
vraag21(con).to_excel(os.path.join(output_dir, "vraag21.xlsx"))
vraag22(con).to_excel(os.path.join(output_dir, "vraag22.xlsx"))
vraag23(con).to_excel(os.path.join(output_dir, "vraag23.xlsx"))
vraag24(con).to_excel(os.path.join(output_dir, "vraag24.xlsx"))
vraag25(con).to_excel(os.path.join(output_dir, "vraag25.xlsx"))
vraag26(con).to_excel(os.path.join(output_dir, "vraag26.xlsx"))
vraag27(con).to_excel(os.path.join(output_dir, "vraag27.xlsx"))
vraag28(con).to_excel(os.path.join(output_dir, "vraag28.xlsx"))
vraag29(con).to_excel(os.path.join(output_dir, "vraag29.xlsx"))
vraag30(con).to_excel(os.path.join(output_dir, "vraag30.xlsx"))
# ## Van Jupyter Notebook naar Pythonproject
#%% md
# 1. Richt de map waarin jullie tot nu toe hebben gewerkt in volgens de mappenstructuur uit de slides.
# 2. Maak van de ontstane mappenstructuur een Pythonproject dat uitvoerbaar is vanuit de terminal. Maak daarin een .py-bestand dat minstens 5 antwoorden uit dit notebook (in de vorm van een DataFrame) exporteert naar Excelbestanden. Alle notebooks mogen als notebook blijven bestaan.
# 3. Zorg ervoor dat dit Pythonproject zijn eigen repo heeft op Github. Let op: je virtual environment moet <b><u>niet</u></b> meegaan naar Github.
# 
# Je mag tijdens dit proces je uit stap 1 ontstane mappenstructuur aanpassen, zolang je bij het beoordelingsmoment kan verantwoorden wat de motivatie hierachter is. De slides verplichten je dus nergens toe.