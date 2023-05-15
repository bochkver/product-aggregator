import logging
import asab
import aiohttp
from urllib.parse import urljoin

L = logging.getLogger(__name__)

class OffersUpdateService(asab.Service):

	def __init__(self, app, service_name, storage, token_repository):
		super().__init__(app, service_name)
		self.OffersHost = asab.Config.get("offers", "host")
		self.Storage = storage
		self.TokenRepository = token_repository
		self.App = app
		# because of free tier DB on Heroku, we would synchronize offers only once an hour
		self.App.PubSub.subscribe("Application.tick/3600!", self.update_offers_table)

	async def update_offers_table(self, _):
		product_ids = self.Storage.get_product_ids()

		for product_id in product_ids:
			offers_from_microservice = await self.request_offers_for_product(product_id)
			keys_offers_from_microservice = [offer['id'] for offer in offers_from_microservice]
			keys_offers_from_database = self.Storage.get_offer_ids_for_product_id(product_id)


			if keys_offers_from_database:
				# delete sold offers from database
				s = set(keys_offers_from_microservice)
				diff = [x for x in keys_offers_from_database if x not in s]
				if diff:
					self.Storage.delete_offers_by_id(product_id, diff)

			for offer in offers_from_microservice:
				self.Storage.store_offer(product_id, offer['id'], offer['price'], offer['items_in_stock'])
		return

	async def request_offers_for_product(self, product_id):
		token = await self.TokenRepository.get_token()
		if token is None:
			return None

		headers = {"Accept": "application/json", "Bearer": token}
		url = urljoin(self.OffersHost, "products/{}/offers".format(product_id))

		async with aiohttp.ClientSession(headers=headers) as session:
			async with session.get(url) as resp:
				if resp.status == 200:
					return await resp.json()
				else:
					L.error("Failed to get offers product. {}".format(await resp.text()))
					return None
