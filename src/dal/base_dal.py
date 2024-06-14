class BaseDAL:
    """
    The base Data Access Layer that defines the interface of the data access.
    """

    def __init__(self) -> None: ...

    def get_location_by_ip(self, ip_address: str) -> tuple[str, str]:
        """
        Return the location (city, country) of the given IP address.
        This method should be overridden by the inheriting DAL classes.

        Returns:
            Tuple of (city, country)
        """
        ...
