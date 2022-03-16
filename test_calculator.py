import unittest
from calculator import User, Product, Order, Order_Details, Promotion, Calculator

class TestOrderClass(unittest.TestCase):
    def setUp(self):
        self.user1 = User(user_id = 1, user_email = 'abc@example.com')
        self.product1 = Product(product_id=1,product_unit_price =30, manufacturer='test')
        self.product2 = Product(product_id=2,product_unit_price =20, manufacturer='test')
        self.product3 = Product(product_id=3,product_unit_price =10, manufacturer='test')
        self.order_details1 = Order_Details(order_details_id=1, order_id = 1, Product=self.product1,product_quantity=5)
        self.order_details2 = Order_Details(order_details_id=2, order_id = 1, Product=self.product2, product_quantity=5)
        self.order_details3 = Order_Details(order_details_id=3, order_id = 1, Product=self.product3,product_quantity=3)
        self.order1 = Order(order_id=1, User=self.user1, order_details = [self.order_details1,self.order_details2,self.order_details3])
        self.order2 = Order(order_id=2, User=self.user1, order_details=[])
        self.order3 = Order(order_id=2, User=self.user1, order_details='test')
    
    # test normal use case and if nothing is in the 'order_details' field
    def test_original_sum(self):
        self.assertEqual(self.order1.original_sum(),280)
        with self.assertRaises(ValueError): #order2 does not contain any order_details
            self.order2.original_sum()

class TestCalculatorClass(unittest.TestCase):
    def setUp(self):
        self.user1 = User(user_id = 1, user_email = 'abc@example.com')
        self.product1 = Product(product_id=1,product_unit_price =30, manufacturer='test')
        self.product2 = Product(product_id=2,product_unit_price =20, manufacturer='test')
        self.product3 = Product(product_id=3,product_unit_price =10, manufacturer='test')
        self.product4 = Product(product_id=4,product_unit_price =100, manufacturer='test')
        self.order_details1 = Order_Details(order_details_id=1, order_id = 1, Product=self.product1,product_quantity=5)
        self.order_details2 = Order_Details(order_details_id=2, order_id = 1, Product=self.product2, product_quantity=5)
        self.order_details3 = Order_Details(order_details_id=3, order_id = 1, Product=self.product3,product_quantity=3)
        self.order1 = Order(order_id=1, User=self.user1, order_details = [self.order_details1,self.order_details2,self.order_details3])
        self.calc = Calculator()

    def test_calculate_plain(self): # 並未使用 promotion
        self.assertEqual(self.calc.calculate(self.order1),{'original_sum': 280, 'deduction': 0, 'deducted_sum': 280})
    
    def test_calculate_item_number_discount(self): # Order 超過 x 數量特定產品折價 $y
        # 設定 promotion 和 order
        self.promotion1 = Promotion(promotion_id=1,limited_product=self.product2,limited_product_threshold=2,decrease_sum=30) 
        self.promotion2 = Promotion(promotion_id=2,limited_product=self.product2,limited_product_threshold=2,decrease_sum=30000)
        self.promotion3 = Promotion(promotion_id=3,limited_product=self.product4,limited_product_threshold=2,decrease_sum=30)
        self.order1 = Order(order_id=1, User=self.user1, order_details = [self.order_details1,self.order_details2,self.order_details3],Promotion=self.promotion1)
        self.order2 = Order(order_id=1, User=self.user1, order_details = [self.order_details1,self.order_details2,self.order_details3],Promotion=self.promotion2)
        self.order3 = Order(order_id=1, User=self.user1, order_details = [self.order_details1,self.order_details2,self.order_details3],Promotion=self.promotion3)
        # 測試
        self.assertEqual(self.calc.calculate(self.order1),{'original_sum': 280, 'deduction': 30, 'deducted_sum': 250}) # 驗證物品數量 promotion 有效
        self.assertEqual(self.calc.calculate(self.order3),{'original_sum': 280, 'deduction': 0, 'deducted_sum': 280}) # 當 promotion 所指定 Product 不等於 promotion.limited_product 
        with self.assertRaises(ValueError): # 當折扣後金額小於等於 0 時，觸發 ValueError
            self.calc.calculate(self.order2)

if __name__ == "__main__":
    unittest.main()

    