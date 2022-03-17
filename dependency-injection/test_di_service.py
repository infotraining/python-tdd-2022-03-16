from unittest.mock import Mock
from dependencies import Injector
import pytest

from di_service_after import BussinessService, ConsoleLogger, DataRepository, WebService


@pytest.fixture
def di():
    class Container(Injector):
        logger = Mock(spec=ConsoleLogger)
        web_service = Mock(spec=WebService)
        data_repository = Mock(spec=DataRepository)
        business_service = BussinessService
    return Container


def test_BusinessService_process_data_logging(di):
    di.web_service.get_data.return_value = '[{"data": [1, "two", 3]}]'
    sut = di.business_service

    sut.process_data()

    assert di.logger.log.call_count == 3


def test_BusinessService_process_data_adds_data_to_repository(di):
    di.web_service.get_data.return_value = '[{"data": [1, "two", 3]}]'
    sut = di.business_service

    sut.process_data()

    di.data_repository.add_data.assert_called_with([1, "two", 3])
