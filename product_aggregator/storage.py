import mysql.connector
import asab
import logging
from mysql.connector import errorcode
from .entities import Product, Offer

L = logging.getLogger(__name__)

class Storage:

	"""
	Storage class is responsible for storing and retrieving data from MySQL database.
	"""

	def __init__(self):
		self.host = asab.Config.get("mysql", "host")
		self.port = asab.Config.get("mysql", "port")
		self.user = asab.Config.get("mysql", "user")
		self.password = asab.Config.get("mysql", "password")
		self.database = asab.Config.get("mysql", "database")

	def get_token(self):
		token = self.fetch("SELECT token, expired FROM tokens WHERE id = 1")
		if token:
			return token[0][0], token[0][1]
		return None

	def store_token(self, token, expiration_date):
		query = "INSERT INTO tokens (id, token, expired) VALUES (1, %s, %s)"
		value = (token, expiration_date)
		self.commit(query, value)

	def delete_token(self):
		self.commit("DELETE from tokens WHERE id = 1")

	def store_product(self, id, name, description):
		query = "INSERT INTO products (product_id, name, description) VALUES (%s, %s, %s)"
		value = (id, name, description)
		if self.commit(query, value):
			return id
		else:
			return None

	def get_product_by_id(self, id):
		query = "SELECT * from products where product_id = %s"
		value = (id,)
		rows = self.fetch(query, value)
		if rows:
			return Product(rows[0][0], rows[0][1], rows[0][2])
		return None

	def delete_product_by_id(self, id):
		query = "DELETE from products WHERE product_id = %s"
		value = (id,)
		if self.commit(query, value):
			return id
		else:
			return None

	def update_product_by_id(self, id, fields):
		set_str = ""
		for field, value in fields:
			set_str += "{} = '{}', ".format(field, value)
		set_str = set_str[:-2]
		query = "UPDATE products SET " + set_str + " WHERE product_id = %s"
		value = (id,)
		if self.commit(query, value):
			return id
		else:
			return None

	def get_product_ids(self):
		query = "SELECT product_id from products"
		return [row[0] for row in self.fetch(query)]

	def get_offers_by_product_id(self, id):
		query = "SELECT * from offers where product_id = %s"
		value = (id,)
		rows = self.fetch(query, value)
		if rows:
			return [Offer(row [0], row[1], row[2], row[3]) for row in rows]
		return None

	def get_offer_ids_for_product_id(self, product_id):
		query = "SELECT offer_id from offers WHERE product_id = %s"
		value = (product_id,)
		return [row[0] for row in self.fetch(query, value)]

	def delete_offers_by_id(self, product_id, offer_ids):
		format_strings = ", ".join(["%s"] * len(offer_ids))
		query = "DELETE from offers WHERE product_id = %s AND offer_id in ({})".format(format_strings)
		value = (product_id,)  + tuple(offer_ids)
		self.commit(query, value)

	def store_offer(self, product_id, offer_id, price, items_in_stock):
		query = "INSERT INTO offers (offer_id, product_id, price, items_in_stock) VALUES (%s, %s, %s, %s)" \
				"ON DUPLICATE KEY UPDATE price= %s, items_in_stock = %s"
		value = (
			offer_id,
			product_id,
			price,
			items_in_stock,
			price,
			items_in_stock
		)
		self.commit(query, value)

	def connect_to_db(self):
		try:
			return mysql.connector.connect(
				host=self.host,
				port=self.port,
				user=self.user,
				password=self.password,
				database=self.database
			)
		except mysql.connector.Error as err:
			if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
				L.error("Something is wrong with your user name or password")
			elif err.errno == errorcode.ER_BAD_DB_ERROR:
				L.error("Database does not exist")
			else:
				L.error(err)
			return None

	def fetch(self, query, values = ()):
		connection = self.connect_to_db()
		try:
			cursor = connection.cursor()
			cursor.execute(query, values)
			result = cursor.fetchall()
			cursor.close()
			connection.close()
			return result
		except Exception as e:
			L.error(e)
			connection.close()
			return None

	def commit(self, query, values = ()):
		connection = self.connect_to_db()
		try:
			cursor = connection.cursor()
			cursor.execute(query, values)
			connection.commit()
			cursor.close()
			connection.close()
			return True
		except Exception as e:
			L.error(e)
			connection.close()
			return None
