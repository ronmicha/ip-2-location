import os

from pandas import read_csv

from src.common.exceptions import DataStoreNotFoundException, IpNotFoundException
from src.dal.base_dal import BaseDAL


class CsvDAL(BaseDAL):
    def __init__(self) -> None:
        super().__init__()

        datastore_path = f"src/datastore/csv_datastore.csv"
        if not os.path.exists(datastore_path):
            raise DataStoreNotFoundException(datastore_path)

        self._datastore_path = datastore_path

    def get_location_by_ip(self, ip_address: str) -> tuple[str, str]:
        # If the datastore CSV is too big to read at once, read it in chunks using `chunksize`
        datastore_df = read_csv(self._datastore_path)
        result_df = datastore_df[datastore_df["ip"] == ip_address]

        if result_df.empty:
            raise IpNotFoundException(ip_address)

        row = result_df.iloc[0]
        return row["city"], row["country"]
