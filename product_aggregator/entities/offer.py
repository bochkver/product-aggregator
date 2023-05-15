class Offer:
    def __init__(self, id, product_id, price, items_in_stock):
        self.id = id
        self.product_id = product_id
        self.price = price
        self.items_in_stock = items_in_stock

    def to_json(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "price": self.price,
            "items_in_stock": self.items_in_stock
        }
