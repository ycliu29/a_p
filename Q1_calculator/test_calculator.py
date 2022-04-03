import unittest
from calculator import User, Product, Order

class TestOrderClass(unittest.TestCase):
    def setUp(self):
        self.product1 = Product(product_id=1,product_unit_price=10)
        self.product2 = Product(product_id=2, product_unit_price=20)
        self.order1 = Order(order_id=1,order_details={self.product1:5,self.product2:10})

    def test_order_sum(self):
        self.assertEqual(self.order1.order_sum(),250)

if __name__ == "__main__":
    unittest.main()