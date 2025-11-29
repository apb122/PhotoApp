"""Database engine and session management utilities."""
from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from .config import Config as AppConfig


class Base(DeclarativeBase):
    """Declarative base class for ORM models."""


engine: Engine | None = None
SessionLocal: sessionmaker[Session] | None = None


def _ensure_database_path(app_config: AppConfig) -> Path:
    database_path = Path(app_config.database_path)
    database_path.parent.mkdir(parents=True, exist_ok=True)
    return database_path


def _build_engine(database_path: Path) -> Engine:
    database_url = f"sqlite+pysqlite:///{database_path}"
    return create_engine(database_url, echo=False, future=True)


def configure_engine(app_config: AppConfig) -> Engine:
    """Create and cache the SQLAlchemy engine from application configuration."""
    global engine
    if engine is not None:
        return engine

    database_path = _ensure_database_path(app_config)
    engine = _build_engine(database_path)
    return engine


def configure_session_factory(target_engine: Engine) -> sessionmaker[Session]:
    """Create and cache the SessionLocal factory for the given engine."""
    global SessionLocal
    if SessionLocal is not None:
        return SessionLocal

    SessionLocal = sessionmaker(bind=target_engine, autoflush=False, expire_on_commit=False)
    return SessionLocal


@contextmanager
def get_session() -> Iterator[Session]:
    """Yield a database session with managed commit/rollback semantics."""
    if SessionLocal is None:
        raise RuntimeError("Session factory not configured. Call init_database() first.")

    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def init_database(app_config: AppConfig) -> Engine:
    """Initialize the database engine, session factory, and create tables."""
    target_engine = configure_engine(app_config)
    configure_session_factory(target_engine)
    Base.metadata.create_all(target_engine)
    return target_engine
