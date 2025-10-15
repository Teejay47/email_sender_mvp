import importlib
import pkgutil
from sqlalchemy import create_engine, inspect
from app.models.base import Base

# 🔹 Database URL from .env or hardcode for now
DATABASE_URL = "postgresql+psycopg2://postgres:postgres@db:5432/email_sender_db"

engine = create_engine(DATABASE_URL)
inspector = inspect(engine)

# Step 1: Get database schema
db_schema = {}
for table_name in inspector.get_table_names():
    db_schema[table_name] = {}
    for col in inspector.get_columns(table_name):
        db_schema[table_name][col["name"]] = {
            "type": str(col["type"]),
            "nullable": col["nullable"],
            "default": col.get("default"),
            "primary_key": col.get("primary_key", False),
        }

# Step 2: Get SQLAlchemy model schema
def iter_models(module_name):
    module = importlib.import_module(module_name)
    for loader, name, is_pkg in pkgutil.iter_modules(module.__path__):
        full_name = f"{module_name}.{name}"
        sub_module = importlib.import_module(full_name)
        for attr_name in dir(sub_module):
            attr = getattr(sub_module, attr_name)
            if isinstance(attr, type) and issubclass(attr, Base) and attr is not Base:
                yield attr

model_schema = {}
for model in iter_models("app.models"):
    table_name = getattr(model, "__tablename__", None)
    if table_name:
        model_schema[table_name] = {}
        for col in model.__table__.columns:
            default_val = col.default.arg if col.default is not None else None
            model_schema[table_name][col.name] = {
                "type": str(col.type),
                "nullable": col.nullable,
                "default": default_val,
                "primary_key": col.primary_key,
            }

# Step 3: Generate SQL to sync DB
print("\n=== SCHEMA FIX SQL ===\n")
for table, cols in model_schema.items():
    if table not in db_schema:
        print(f"-- ⚠️ Table missing: {table}")
        create_sql = f"CREATE TABLE {table} (\n"
        col_defs = []
        pk_cols = []
        for col_name, col_info in cols.items():
            col_def = f"  {col_name} {col_info['type']}"
            if not col_info["nullable"]:
                col_def += " NOT NULL"
            if col_info["default"] is not None:
                col_def += f" DEFAULT {col_info['default']}"
            col_defs.append(col_def)
            if col_info["primary_key"]:
                pk_cols.append(col_name)
        if pk_cols:
            col_defs.append(f"  PRIMARY KEY ({', '.join(pk_cols)})")
        create_sql += ",\n".join(col_defs)
        create_sql += "\n);\n"
        print(create_sql)
        continue

    db_cols = db_schema[table]
    for col_name, col_info in cols.items():
        if col_name not in db_cols:
            default_sql = f"DEFAULT {col_info['default']}" if col_info["default"] is not None else ""
            nullable_sql = "" if col_info["nullable"] else "NOT NULL"
            print(f"ALTER TABLE {table} ADD COLUMN {col_name} {col_info['type']} {nullable_sql} {default_sql};")
            if col_info["primary_key"]:
                print(f"-- ⚠️ Ensure sequence for PK {table}.{col_name} is created if needed")
        else:
            db_col = db_cols[col_name]
            if col_info["nullable"] != db_col["nullable"]:
                if not col_info["nullable"]:
                    print(f"ALTER TABLE {table} ALTER COLUMN {col_name} SET NOT NULL;")
                else:
                    print(f"ALTER TABLE {table} ALTER COLUMN {col_name} DROP NOT NULL;")
            if str(col_info["type"]) != str(db_col["type"]):
                print(f"-- ⚠️ Type mismatch for {table}.{col_name}: Model={col_info['type']} DB={db_col['type']} (manual fix may be needed)")

    # Extra DB columns not in models
    for db_col in db_cols:
        if db_col not in cols:
            print(f"-- ⚠️ Extra column in DB not in model: {table}.{db_col}")
