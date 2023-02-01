import sqlalchemy.ext.declarative as dec
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

SqlAlchemyBase = dec.declarative_base()

__factory = None


def global_init(user, password, host, port, dbname):
    global __factory

    if __factory:
        return
    conn_str = f'postgresql+asyncpg://{user}:{password}@{host}:{port}/{dbname}'
    engine = create_engine(conn_str, pool_pre_ping=True)

    # Создание всех таблиц
    with engine.begin() as conn:
        # conn.run_sync(SqlAlchemyBase.metadata.drop_all)
        conn.run_sync(SqlAlchemyBase.metadata.create_all)

    __factory = sessionmaker(
        engine, expire_on_commit=False, class_=Session
    )


def create_session() -> Session:
    global __factory
    return __factory()
