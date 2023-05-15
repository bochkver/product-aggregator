import asab
import uuid
import pytest
from product_aggregator.aggregator.service import AggregatorService

pytest_plugins = ('pytest_asyncio', 'pytest_mock')

@pytest.mark.asyncio
async def test_create(monkeypatch, mocker):
    app = asab.Application()

    id = uuid.uuid4()
    def static_uuid():
        return id
    def mockreturn(a, b):
        return "/abc"
    async def mockskip(a, b):
        return "/abc"

    monkeypatch.setattr(asab.Config, "get", mockreturn)
    monkeypatch.setattr(AggregatorService, "register_product", mockskip)
    monkeypatch.setattr(uuid, "uuid4", static_uuid)

    storage = mocker.patch('product_aggregator.storage.Storage')
    storage.store_product.return_value = str(id)

    service = AggregatorService(app, "AggregatorService", storage, None)
    json_data = {
        "name": "test",
        "description": "testdesc"
    }

    result = await service.create(json_data)
    assert storage.store_product.called is True
    assert storage.store_product.call_count == 1
    assert storage.store_product.call_args == mocker.call(result, "test", "testdesc")
    assert result == str(id)
