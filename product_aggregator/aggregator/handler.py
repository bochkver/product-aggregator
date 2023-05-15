import asab
import asab.web.rest


class AggregatorWebHandler(object):
	def __init__(self, app, svc):
		self.Service = svc
		web_app = app.WebContainer.WebApp

		web_app.router.add_post("/products/create", self.create)
		web_app.router.add_get("/products/{id}", self.read)
		web_app.router.add_delete("/products/{id}", self.delete)
		web_app.router.add_put("/products/{id}", self.update)
		web_app.router.add_get("/offers/{product_id}", self.read_offers)

	@asab.web.rest.json_schema_handler({
			"type": "object",
			"properties": {
				"name": {"type": "string"},
				"description": {"type": "string"},
			},
			"required": ["name", "description"]
		}
	)
	async def create(self, request, json_data):
		result = await self.Service.create(json_data)
		if result is None:
			response = {
				"result": "FAILED"
			}
		else:
			response = {
				"result": "OK",
				"data": {
					"id": result
				}
			}
		return asab.web.rest.json_response(request, response)

	async def read(self, request):
		id = request.match_info["id"]
		result = await self.Service.read(id)
		if result is None:
			response = {
				"result": "FAILED"
			}
		else:
			response = {
				"result": "OK",
				"data":	result.to_json()
			}
		return asab.web.rest.json_response(request, response)

	async def delete(self, request):
		id = request.match_info["id"]
		result = await self.Service.delete(id)
		if result is None:
			response = {
				"result": "FAILED"
			}
		else:
			response = {
				"result": "OK",
				"data": {
					"id": result
				}
			}
		return asab.web.rest.json_response(request, response)

	@asab.web.rest.json_schema_handler({
			"type": "object",
			"properties": {
				"name": {"type": "string"},
				"description": {"type": "string"},
			}
		}
	)
	async def update(self, request, json_data):
		id = request.match_info["id"]
		result = await self.Service.update(id, json_data)
		if result is None:
			response = {
				"result": "FAILED"
			}
		else:
			response = {
				"result": "OK",
				"data": {
					"id": result
				}
			}
		return asab.web.rest.json_response(request, response)

	async def read_offers(self, request):
		id = request.match_info["product_id"]
		result = await self.Service.read_offers(id)
		if result is None:
			response = {
				"result": "FAILED"
			}
		else:
			response = {
				"result": "OK",
				"data":	[el.to_json() for el in result]
			}
		return asab.web.rest.json_response(request, response)
