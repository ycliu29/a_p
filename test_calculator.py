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
        # 基礎假設
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

    # 訂單未使用 promotion
    def test_calculate_plain(self): 
        self.assertEqual(self.calc.calculate(self.order1),{'original_sum': 280, 'deduction': 0, 'deducted_sum': 280})
    
    # 特定商品滿 X 件折 Y 元
    def test_calculate_item_number_discount(self): 
        # 測試假設
        self.promotion1 = Promotion(promotion_id=1,limited_product=self.product2,limited_product_threshold=2,decrease_sum=30) 
        self.promotion2 = Promotion(promotion_id=2,limited_product=self.product2,limited_product_threshold=2,decrease_sum=30000)
        self.promotion3 = Promotion(promotion_id=3,limited_product=self.product4,limited_product_threshold=2,decrease_sum=30)
        self.order1 = Order(order_id=1, User=self.user1, order_details = [self.order_details1,self.order_details2,self.order_details3],Promotion=self.promotion1)
        self.order2 = Order(order_id=1, User=self.user1, order_details = [self.order_details1,self.order_details2,self.order_details3],Promotion=self.promotion2)
        self.order3 = Order(order_id=1, User=self.user1, order_details = [self.order_details1,self.order_details2,self.order_details3],Promotion=self.promotion3)

        # 測試
        # 驗證物品數量 promotion 有效
        self.assertEqual(self.calc.calculate(self.order1),{'original_sum': 280, 'deduction': 30, 'deducted_sum': 250}) 
        # 當 promotion 所指定 Product 不等於 promotion.limited_product，不觸發
        self.assertEqual(self.calc.calculate(self.order3),{'original_sum': 280, 'deduction': 0, 'deducted_sum': 280}) 
        # 當折扣後金額小於等於 0 時，觸發 ValueError
        with self.assertRaises(ValueError): 
            self.calc.calculate(self.order2)

    # 訂單滿 X 元贈送特定商品
    def test_calculate_free_item(self): 
        # 測試假設
        self.promotion1 = Promotion(promotion_id=1,threshold=100,free_item=self.product1)
        self.order1 = Order(order_id=1, User=self.user1, order_details = [self.order_details1,self.order_details2,self.order_details3],Promotion=self.promotion1)
        self.order2 = Order(order_id=2, User=self.user1, order_details = [self.order_details3],Promotion=self.promotion1)

        # 測試 免費商品於 deduction 以 product_id 表示
        # 一般測試，正常回傳 free product_id 於 deduction
        self.assertEqual(self.calc.calculate(self.order1),{'original_sum': 280, 'deduction': 'free_product_id: 1', 'deducted_sum': 280})
        # 價格未達 threshold 不觸發 promotion
        self.assertEqual(self.calc.calculate(self.order2),{'original_sum': 30, 'deduction': 0 , 'deducted_sum': 30})

    # 訂單滿 X 元折 Z %
    def test_calculate_decrease_percentage_no_decreaselimit(self):
        # 測試假設
        self.promotion1 = Promotion(promotion_id=1,threshold=100,decrease_percentage=0.05)
        self.order1 = Order(order_id=1, User=self.user1, order_details = [self.order_details1,self.order_details2,self.order_details3],Promotion=self.promotion1)
        self.promotion2 = Promotion(promotion_id=2,threshold=100,decrease_percentage=0.07)
        self.order2 = Order(order_id=1, User=self.user1, order_details = [self.order_details1,self.order_details2,self.order_details3],Promotion=self.promotion2)

        # 一般測試，折扣後無小數點 280*0.05 = 14
        self.assertEqual(self.calc.calculate(self.order1),{'original_sum': 280, 'deduction': 14, 'deducted_sum': 266})
        # 一般測試，折扣後無有數點 280*0.07 = 19.6，捨去小數點
        self.assertEqual(self.calc.calculate(self.order2),{'original_sum': 280, 'deduction': 19, 'deducted_sum': 261})

if __name__ == "__main__":
    unittest.main()

    