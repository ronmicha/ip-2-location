import os
from contextvars import ContextVar
from typing import Type

from src.common.consts import DATASTORE_TYPE_ENV_VAR, DEFAULT_DATASTORE_TYPE
from src.common.exceptions import DALClassNotFoundException
from src.dal.base_dal import BaseDAL
from src.dal.csv_dal import CsvDAL

dal_instance_var: ContextVar[BaseDAL] = ContextVar("dal_instance")

DATASTORE_TYPE_TO_DAL: dict[str, Type[BaseDAL]] = {
    "csv": CsvDAL,
}


def set_dal_instance() -> None:
    datastore_type = os.getenv(DATASTORE_TYPE_ENV_VAR, DEFAULT_DATASTORE_TYPE)

    dal_class = DATASTORE_TYPE_TO_DAL.get(datastore_type)
    if dal_class is None:
        raise DALClassNotFoundException(datastore_type)

    dal_instance = dal_class()
    dal_instance_var.set(dal_instance)


def get_dal_instance() -> BaseDAL:
    return dal_instance_var.get()
