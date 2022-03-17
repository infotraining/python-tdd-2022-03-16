
import abc
import json
from dependencies import Injector


class ConsoleLogger:
    def __init__(self, log_filename):
        self._log_filename = log_filename
        self._counter = 0

    def log(self, msg):
        self._counter += 1
        print(f"LOG:{self._counter} - {self._log_filename}: {msg}")


class WebService:
    def __init__(self, url_address):
        self._url_address = url_address

    def get_data(self):
        data = json.dumps([{'from': f'{self._url_address}', 'data': [
            1, 'two', 3]}], sort_keys=True, indent=4)
        return data


class DataRepository:
    def __init__(self, logger):
        self._logger = logger
        self._data = []

    def add_data(self, data):
        self._logger.log(f"Adding {data!r} to repository")
        self._data.append(data)


class BussinessService:
    def __init__(self, web_service, data_repository, logger):
        # WebService("http://datavault.com/data")
        self._web_service = web_service
        self._data_repository = data_repository
        self._logger = logger

    def process_data(self):
        self._logger.log("Start processing")
        data = self._web_service.get_data()
        json_data = json.loads(data)
        self._logger.log(f"Data loaded: {json_data!r}")
        self._data_repository.add_data(json_data[0]['data'])
        self._logger.log("End processing")


class Container(Injector):
    log_filename = "business_service.log"
    logger = ConsoleLogger
    url_address = "http://datavault.com/data"
    web_service = WebService
    data_repository = DataRepository
    business_service = BussinessService


if __name__ == "__main__":
    bs = Container.business_service

    bs.process_data()

    print("*"*40)

    other_bs = Container.business_service
    other_bs.process_data()
