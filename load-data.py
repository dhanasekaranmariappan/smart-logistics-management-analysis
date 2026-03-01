import pandas as pd
from sqlalchemy import create_engine, text, VARCHAR, DECIMAL, DATE, INT, DATETIME
import os
from dotenv import load_dotenv
from urllib.parse import quote

load_dotenv()

db_user = os.getenv("DB_USER")
db_host = os.getenv("DB_HOST")
db_password = os.getenv("DB_PASSWORD")
db_port = int(os.getenv("DB_PORT"))
db_name = os.getenv("DB_NAME")

encoded_password = quote(db_password, safe='')
engine = create_engine(
    f'mysql+mysqlconnector://{db_user}:{encoded_password}@{db_host}:{db_port}/{db_name}'
)

try:
    # Step 1 — Disable FK checks
    with engine.connect() as conn:
        conn.execute(text("SET FOREIGN_KEY_CHECKS=0;"))
        conn.commit()
    print(" Foreign key checks disabled.")

    # Step 2 — Read all files
    costs_df = pd.read_csv('datafiles/costs.csv')
    couriers_df = pd.read_csv('datafiles/courier_staff.csv')
    routes_df = pd.read_csv('datafiles/routes.csv')
    tracking_df = pd.read_csv('datafiles/shipment_tracking.csv')
    # read all JSON files
    shipments_df = pd.read_json('datafiles/shipments.json')
    warehouses_df = pd.read_json('datafiles/warehouses.json')

    # Step 3 — Deduplicate data
    shipments_df = shipments_df.drop_duplicates(subset='shipment_id', keep='first')
    print(f"Shipments after dedup: {len(shipments_df)}")  

    costs_df = costs_df.drop_duplicates(subset='shipment_id', keep='first')
    print(f"Costs after dedup: {len(costs_df)}")  

    # Step 4 — Load tables
    print("Loading courier_staff...")
    couriers_df.to_sql('courier_staff', engine, if_exists='replace', index=False,
        chunksize=1000,
        dtype={
            'courier_id': VARCHAR(50),
            'name': VARCHAR(150),
            'rating': DECIMAL(3, 1),
            'vehicle_type': VARCHAR(50)  # fixed typo
        }
    )

    print("Loading warehouses...")
    warehouses_df.to_sql('warehouses', engine, if_exists='replace', index=False,
        chunksize=1000,
        dtype={
            'warehouse_id': VARCHAR(50),
            'city': VARCHAR(100),
            'state': VARCHAR(50),
            'capacity': INT()
        }
    )

    print("Loading routes...")
    routes_df.to_sql('routes', engine, if_exists='replace', index=False,
        chunksize=1000,
        dtype={
            'route_id': VARCHAR(50),
            'origin': VARCHAR(100),
            'destination': VARCHAR(100),
            'distance_km': DECIMAL(10, 2),
            'avg_time_hours': DECIMAL(5, 2)
        }
    )

    print("Loading shipments...")
    shipments_df.to_sql('shipments', engine, if_exists='replace', index=False,
        chunksize=1000,
        dtype={
            'shipment_id': VARCHAR(50),
            'order_date': DATE(),
            'origin': VARCHAR(100),
            'destination': VARCHAR(100),
            'weight': DECIMAL(10, 2),
            'courier_id': VARCHAR(50),
            'status': VARCHAR(50),
            'delivery_date': DATE()
        }
    )

    print("Loading costs...")
    costs_df.to_sql('costs', engine, if_exists='replace', index=False,
        chunksize=1000,
        dtype={
            'shipment_id': VARCHAR(50),
            'fuel_cost': DECIMAL(15, 2),
            'labor_cost': DECIMAL(15, 2),
            'misc_cost': DECIMAL(15, 2)
        }
    )

    print("Loading shipment_tracking...")
    tracking_df.to_sql('shipment_tracking', engine, if_exists='replace', index=False,
        chunksize=1000,
        dtype={
            'tracking_id': INT(),
            'shipment_id': VARCHAR(50),
            'status': VARCHAR(50),
            'timestamp': DATETIME()
        }
    )

    print(" All data loaded successfully!")

    # Step 5 — Add Primary Keys (inside try, after loading)
    with engine.connect() as conn:
        conn.execute(text("ALTER TABLE courier_staff ADD PRIMARY KEY (courier_id);"))
        conn.execute(text("ALTER TABLE warehouses ADD PRIMARY KEY (warehouse_id);"))
        conn.execute(text("ALTER TABLE routes ADD PRIMARY KEY (route_id);"))
        conn.execute(text("ALTER TABLE shipments ADD PRIMARY KEY (shipment_id);"))
        conn.execute(text("ALTER TABLE costs ADD PRIMARY KEY (shipment_id);"))
        conn.execute(text("ALTER TABLE shipment_tracking ADD PRIMARY KEY (tracking_id);"))
        conn.commit()
    print(" Primary keys added!")

    # Step 6 — Add Foreign Keys (inside try, after PKs)
    with engine.connect() as conn:
        conn.execute(text("""
            ALTER TABLE shipments ADD CONSTRAINT fk_shipments_courier
            FOREIGN KEY (courier_id) REFERENCES courier_staff(courier_id);
        """))
        conn.execute(text("""
            ALTER TABLE costs ADD CONSTRAINT fk_costs_shipment
            FOREIGN KEY (shipment_id) REFERENCES shipments(shipment_id);
        """))
        conn.execute(text("""
            ALTER TABLE shipment_tracking ADD CONSTRAINT fk_tracking_shipment
            FOREIGN KEY (shipment_id) REFERENCES shipments(shipment_id);
        """))
        conn.commit()
    print(" Foreign key constraints added!")

except Exception as e:
    print(f" Error occurred: {e}")

finally:
    # Always re-enable FK checks no matter what
    with engine.connect() as conn:
        conn.execute(text("SET FOREIGN_KEY_CHECKS=1;"))
        conn.commit()
    print(" Foreign key checks re-enabled.")