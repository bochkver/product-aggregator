import asab
import asab.web
import asab.web.rest
import asab.storage
import logging
import os

from .storage import Storage

L = logging.getLogger(__name__)

asab.Config.add_defaults(
{
        "web": {
                "listen": "0.0.0.0 8080"
        },
		"mysql": {
			"host": "db",
			"port": 3306,
			"user": "root",
			"password": "qwerty",
			"database": "db"
		}
})

class ProductAggregatorApp(asab.Application):

	def __init__(self):
		super().__init__()
		# Register modules
		self.add_module(asab.web.Module)


		# Locate the web service
		self.WebService = self.get_service("asab.WebService")
		self.WebContainer = asab.web.WebContainer(
				self.WebService, "web"
		)
		self.WebContainer.WebApp.middlewares.append(
				asab.web.rest.JsonExceptionMiddleware
		)

		# Initialize services
		self.Storage = Storage()
