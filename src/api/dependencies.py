import ipaddress

from fastapi import Query

from src.common.exceptions import InvalidIPAddressException


def validate_ip_address(ip: str = Query(...)) -> str:
    try:
        ipaddress.ip_address(ip)
        return ip
    except ValueError:
        raise InvalidIPAddressException(ip)
