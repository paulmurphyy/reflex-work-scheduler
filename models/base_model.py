import reflex as rx
from pydantic import ConfigDict
from sqlmodel import Field, SQLModel

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class SimpleModel(rx.Model):
    """Base model for everything."""

    model_config = ConfigDict(
        protected_namespaces=(),
    )  # type: ignore


SimpleModel.metadata.naming_convention = convention