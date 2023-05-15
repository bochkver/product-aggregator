import asab
import aiohttp
import logging
from urllib.parse import urljoin
from datetime import datetime, timedelta

L = logging.getLogger(__name__)

class TokenRepository:
	"""
	TokenRepository is responsible for storing, retrieving and updating access token for Offers API.
	"""

	def __init__(self, storage):
		self.Storage = storage
		self.OffersHost = asab.Config.get("offers", "host")
		self.AuthToken = asab.Config.get("offers", "token")

	async def get_token(self):
		token = self.get_stored_token()
		if token:
			return token
		token = await self.request_new_token()
		if token:
			now = datetime.now()
			expiration_date = now + timedelta(minutes=5)
			self.Storage.store_token(token, expiration_date)
			return token
		# we requested new token, but received error
		# handle me somehow
		return None

	def get_stored_token(self):
		token = self.Storage.get_token()
		if token:
			# check expiration date
			expired = token[1]
			if expired > datetime.now():
				return token[0]

			# if expired, delete token from db
			self.Storage.delete_token()
		return None

	async def request_new_token(self):
		url = urljoin(self.OffersHost, "auth")
		headers = {"Accept": "application/json", "Bearer": self.AuthToken}
		async with aiohttp.ClientSession(headers=headers) as session:
			async with session.post(url) as resp:
				if resp.status == 201:
					content = await resp.json()
					return content["access_token"]
				else:
					L.error("Failed to generate access token. {}".format(await resp.text()))
					return None
