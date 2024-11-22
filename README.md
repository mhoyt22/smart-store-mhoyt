# smart-store-mhoyt

## Table of Contents
- [smart-store-mhoyt](#smart-store-mhoyt)
  - [Table of Contents](#table-of-contents)
  - [Project Setup](#project-setup)
  - [Data Preparation](#data-preparation)
  - [Data Warehouse](#data-warehouse)
    - [Create Data Warehouse (one-time process)](#create-data-warehouse-one-time-process)
    - [Schema](#schema)
      - [customers](#customers)
      - [products](#products)
      - [sales](#sales)
    - [ETL to DW](#etl-to-dw)
  - [Commit to GitHub](#commit-to-github)

## Project Setup
Run all commands from a terminal in the root project folder.

Step 1 - Create a Local Project Virtual Environment
```bash
py -m venv .venv
```

Step 2 - Activate the Virtual Environment
```bash
.venv\Scripts\activate
```

Step 3 - Install Packages
```bash
py -m pip install --upgrade -r requirements.txt
```

Step 4 - Optional: Verify .venv Setup
```bash
py -m datafun_venv_checker.venv_checker
```

## Data Preparation

Step 1: Create data_scrubber class <br>
Step 2: Create data_prep script <br>
Step 3: Run data_prep sript <br>
```bash
py scripts\data_prep.py
```
## Data Warehouse

### Create Data Warehouse (one-time process)
```bash
py scripts\create_dw.py
```

### Schema

#### <u>customers</u>
```bash
Table Type: Dimension
Pimary key: customer_id
Foreign Key(s):
```
| Column Name               | Data Type | Description                        |
|---------------------------|-----------|------------------------------------|
| customer_id               | INTEGER   | Primary Key                        |
| name                      | TEXT      | Name of the customer               |
| region                    | TEXT      | Region where customer resides      |
| join_date                 | DATE      | Date when the customer joined      |
| loyalty_points            | INTEGER   | Total loyalty points for customer  |
| preferred_contact_method  | TEXT      | Preferred contact method           |


#### <u>products</u>
```bash
Table Type: Dimension
Pimary key: product_id
Foreign Key(s):
```
| Column Name     | Data Type | Description                   |
|-----------------|-----------|-------------------------------|
| product_id      | INTEGER   | Primary key                   |
| product_name    | TEXT      | Name of the product           |
| category        | TEXT      | Category of the product       |
| unit_price      | REAL      | Price per unit of the product |
| stock_quantity  | INTEGER   | Quantity in stock             |
| supplier        | TEXT      | Supplier of product           |

#### <u>sales</u>
```bash
Table Type: Fact
Pimary key: transaction_id
Foreign Key(s): customer_id, product_id, store_id, campaign_id
```
| Column Name       | Data Type | Description                  |
|-------------------|-----------|------------------------------|
| transaction_id    | INTEGER   | Primary Key                  |
| sales_date        | DATE      | Date of the transaction      |
| customer_id       | INTEGER   | Foreign key to customers     |
| product_id        | INTEGER   | Foreign key to products      |
| store_id          | INTEGER   | Foreign key to Stores        |
| campaign_id       | INTEGER   | Foreign key to Campaigns     |
| sales_amount      | REAL      | Total sales amount           |
| discount_percent  | INTEGER   | Total discount percent       |
| payment_type      | TEXT      | Payment type used            |

### ETL to DW
```bash
py scripts\create_dw.py
```

## Commit to GitHub

Step 1 – Add All New Files to Source Control
```bash
git add .
```

Step 2 - Commit with a Message Describing Changes
```bash
git commit -m "INSERT COMMENT HERE"
```

Step 3 - Push the Changes to the Origin on Branch `main`
```bash
git push -u origin main
```
