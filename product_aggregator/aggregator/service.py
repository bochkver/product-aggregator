import asab
import uuid
import logging
import aiohttp
import json
from urllib.parse import urljoin

L = logging.getLogger(__name__)

class AggregatorService(asab.Service):

	def __init__(self, app, service_name, storage, token_repository):
		super().__init__(app, service_name)
		self.OffersHost = asab.Config.get("offers", "host")
		self.Storage = storage
		self.App = app
		self.TokenRepository = token_repository

	async def create(self, json_data):
		obj_id = str(uuid.uuid4())
		name = json_data.get("name")
		description = json_data.get("description")
		json_data['id'] = obj_id
		product_id = self.Storage.store_product(obj_id, name, description)
		if product_id is None:
			return None
		await self.register_product(json.dumps(json_data))
		return product_id

	async def read(self, id):
		return self.Storage.get_product_by_id(id)

	async def delete(self, id):
		return self.Storage.delete_product_by_id(id)

	async def update(self, id, json_data):
		return self.Storage.update_product_by_id(id, json_data.items())

	async def register_product(self, json_data):
		url = urljoin(self.OffersHost, "products/register")

		token = await self.TokenRepository.get_token()
		if token is None:
			# error, we cannot register product
			return
		headers = {'Content-Type': 'application/json', 'Bearer': token}

		async with aiohttp.ClientSession(headers=headers) as session:
			async with session.post(url,data=json_data) as resp:
				if resp.status == 201:
					content = await resp.json()
					L.warning("Product registered. {}".format(content))
				else:
					L.error("Failed to register product. {}".format(await resp.text()))
					return

	async def read_offers(self, id):
		return self.Storage.get_offers_by_product_id(id)