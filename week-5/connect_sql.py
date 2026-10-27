from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    Unicode,
    ForeignKey,
    PrimaryKeyConstraint,
    text,
    inspect
)
from sqlalchemy.engine import URL


# --------------------------------------------------
# 1. SQL SERVER CONNECTION SETTINGS
# --------------------------------------------------

SERVER = r"localhost\SQLSERVER2019"
DATABASE = "StarWarsDB"
DRIVER = "ODBC Driver 18 for SQL Server"


def make_connection_url(database_name):
    odbc_connection = (
        f"DRIVER={{{DRIVER}}};"
        f"SERVER={SERVER};"
        f"DATABASE={database_name};"
        "Trusted_Connection=yes;"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
    )

    return URL.create(
        "mssql+pyodbc",
        query={"odbc_connect": odbc_connection}
    )


# --------------------------------------------------
# 2. CREATE THE DATABASE IF NECESSARY
# --------------------------------------------------

master_engine = create_engine(make_connection_url("master"))

with master_engine.connect().execution_options(
    isolation_level="AUTOCOMMIT"
) as connection:
    connection.execute(text("""
        IF DB_ID(N'StarWarsDB') IS NULL
            CREATE DATABASE StarWarsDB;
    """))

master_engine.dispose()


# --------------------------------------------------
# 3. CONNECT TO THE PROJECT DATABASE
# --------------------------------------------------

engine = create_engine(make_connection_url(DATABASE))
metadata = MetaData()


# --------------------------------------------------
# 4. STARSHIPS TABLE
# --------------------------------------------------

starships = Table(
    "Starships",
    metadata,

    Column("StarshipID", Integer, primary_key=True, autoincrement=False),
    Column("MongoID", String(50), nullable=False, unique=True),

    Column("Name", Unicode(150), nullable=False),
    Column("Model", Unicode(200)),
    Column("Manufacturer", Unicode(500)),

    Column("CostInCredits", String(50)),
    Column("Length", String(50)),
    Column("MaxAtmospheringSpeed", String(100)),
    Column("Crew", String(100)),
    Column("Passengers", String(100)),
    Column("CargoCapacity", String(100)),
    Column("Consumables", String(100)),
    Column("HyperdriveRating", String(50)),
    Column("MGLT", String(50)),
    Column("StarshipClass", Unicode(150)),

    Column("Created", String(50)),
    Column("Edited", String(50)),
    Column("URL", String(255))
)


# --------------------------------------------------
# 5. PILOTS TABLE
# --------------------------------------------------

pilots = Table(
    "Pilots",
    metadata,

    Column("PilotMongoID", String(50), primary_key=True),
    Column("PilotName", Unicode(150), nullable=False)
)


# --------------------------------------------------
# 6. STARSHIP-PILOT LINKING TABLE
# --------------------------------------------------

starship_pilots = Table(
    "StarshipPilots",
    metadata,

    Column(
        "StarshipID",
        Integer,
        ForeignKey("Starships.StarshipID"),
        nullable=False
    ),

    Column(
        "PilotMongoID",
        String(50),
        ForeignKey("Pilots.PilotMongoID"),
        nullable=False
    ),

    PrimaryKeyConstraint("StarshipID", "PilotMongoID")
)


# --------------------------------------------------
# 7. CREATE TABLES AND TEST CONNECTION
# --------------------------------------------------

RESET_TABLES = True   # set to False once the schema is stable

if RESET_TABLES:
    metadata.drop_all(engine)
metadata.create_all(engine)

with engine.connect() as connection:
    print("SQL Server connection successful!")
    print("Database:", DATABASE)
    print("Tables:", inspect(engine).get_table_names())
