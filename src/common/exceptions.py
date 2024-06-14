from fastapi import HTTPException


class InvalidIPAddressException(HTTPException):
    def __init__(self, ip_address: str) -> None:
        message = f"Invalid IP address: {ip_address}"
        super().__init__(status_code=400, detail=message)


class DALClassNotFoundException(HTTPException):
    def __init__(self, datastore_name: str) -> None:
        message = f"No DAL class found for datastore name: {datastore_name}"
        super().__init__(status_code=500, detail=message)


class DataStoreNotFoundException(HTTPException):
    def __init__(self, datastore_path: str) -> None:
        message = f"Data store was not found at: {datastore_path}"
        super().__init__(status_code=500, detail=message)


class IpNotFoundException(HTTPException):
    def __init__(self, ip_address: str) -> None:
        message = (
            f"The following IP address was not found in the datastore: {ip_address}"
        )
        super().__init__(status_code=404, detail=message)
