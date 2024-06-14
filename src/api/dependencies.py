import ipaddress
import os
from typing import Type

from fastapi import Depends, Query

from src.common.consts import DATASTORE_TYPE_ENV_VAR, DEFAULT_DATASTORE_TYPE
from src.common.exceptions import DALClassNotFoundException, InvalidIPAddressException
from src.dal.base_dal import BaseDAL
from src.dal.csv_dal import CsvDAL

DATASTORE_TYPE_TO_DAL: dict[str, Type[BaseDAL]] = {
    "csv": CsvDAL,
}


def validate_ip_address(ip: str = Query(...)) -> str:
    try:
        ipaddress.ip_address(ip)
        return ip
    except ValueError:
        raise InvalidIPAddressException(ip)


# The `Depends` param here enforces the dependecies order - validate the IP first, and then get the DAL instance
def get_dal_instance(ip: str = Depends(validate_ip_address)) -> BaseDAL:
    datastore_type = os.getenv(DATASTORE_TYPE_ENV_VAR, DEFAULT_DATASTORE_TYPE)

    dal_class = DATASTORE_TYPE_TO_DAL.get(datastore_type)
    if dal_class is None:
        raise DALClassNotFoundException(datastore_type)

    dal_instance = dal_class()
    return dal_instance
