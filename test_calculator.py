import unittest
from calculator import User, Product, Order, Order_Details, Promotion, Calculator

# 測試 Order.original_sum() 方法 
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
    
    # 測試 original_sum method 及若訂單無 order_details
    def test_original_sum(self):
        # 正常計算訂單總額（無 promotion）
        self.assertEqual(self.order1.original_sum(),280)
        # order2 結帳金額為 0，觸發 ValieError('Order sum cannot be less than or equal to zero')
        with self.assertRaises(ValueError): 
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
        # 訂單總額為 5*30 + 5*20 + 3*10 = 280
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
        # promotion1 為若訂單有 >= 2 個 Product2，折 30，有效
        self.assertEqual(self.calc.calculate(self.order1),{'original_sum': 280, 'deduction': 30, 'deducted_sum': 250}) 
        # promotion3 為若訂單有 >= 2 個 Product4，折 30，Product4 不在 OrderDetails 中，不觸發
        self.assertEqual(self.calc.calculate(self.order3),{'original_sum': 280, 'deduction': 0, 'deducted_sum': 280}) 
        # promotion2 為若訂單有 >= 2 個 Produtc2，折 30000，折扣後 deducted_sum <= 0，觸發 ValueError('Order sum cannot be less than or equal to zero')
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
        # 一般測試，折扣後有小數點 280*0.07 = 19.6，捨去小數點
        self.assertEqual(self.calc.calculate(self.order2),{'original_sum': 280, 'deduction': 19, 'deducted_sum': 261})

    # 訂單滿 X 元折 Z %，折扣每人只能總共優惠 N 元
    def test_calculate_decrease_percentage_with_decreaselimit(self):
        self.promotion1 = Promotion(promotion_id=1,threshold=100,decrease_percentage=0.3,decrease_sum_limit=10)
        self.order1 = Order(order_id=1, User=self.user1, order_details = [self.order_details1,self.order_details2,self.order_details3],Promotion=self.promotion1)
        self.promotion2 = Promotion(promotion_id=2,threshold=100,decrease_percentage=0.05, decrease_sum_limit=100)
        self.order2 = Order(order_id=1, User=self.user1, order_details = [self.order_details1,self.order_details2,self.order_details3],Promotion=self.promotion2)

        # 測試
        # 一般測試，折扣後無小數點 280*0.3 = 84 但折扣 <= 10
        self.assertEqual(self.calc.calculate(self.order1),{'original_sum': 280, 'deduction': 10, 'deducted_sum': 270})
        # 一般測試，折扣後無小數點 280*0.05 = 14 折扣限額為 100
        self.assertEqual(self.calc.calculate(self.order2),{'original_sum': 280, 'deduction': 14, 'deducted_sum': 266})

    # 訂單滿 X 元折 Y 元，此折扣在全站總共只能套⽤ N 次
    def test_calculate_decrease_sum_usage_count_limit(self):
        self.promotion1 = Promotion(promotion_id=1,threshold=100,decrease_sum=30,usage_count_limit=1000,usage_used_count=980)
        self.order1 = Order(order_id=1, User=self.user1, order_details = [self.order_details1,self.order_details2,self.order_details3],Promotion=self.promotion1)
        self.promotion2 = Promotion(promotion_id=2,threshold=100,decrease_sum=50,usage_count_limit=1000,usage_used_count=1000)
        self.order2 = Order(order_id=1, User=self.user1, order_details = [self.order_details1,self.order_details2,self.order_details3],Promotion=self.promotion2)

        # 測試
        # 折扣為滿 100 折 30，使用次數未達全站上限
        self.assertEqual(self.calc.calculate(self.order1),{'original_sum': 280, 'deduction': 30, 'deducted_sum': 250})
        # 折扣為滿 100 折 50，使用次數已達全站上限，折扣無效
        self.assertEqual(self.calc.calculate(self.order2),{'original_sum': 280, 'deduction': 0, 'deducted_sum': 280})

    # 訂單滿 X 元折 Y 元，此折扣在全站每個⽉折扣上限為 N 元
    def test_calculate_decrease_sum_monthly_sum_limit(self):
        self.promotion1 = Promotion(promotion_id=1,threshold=100,decrease_sum=30,monthly_sum_limit=10000,monthly_sum_used=10000)
        self.order1 = Order(order_id=1, User=self.user1, order_details = [self.order_details1,self.order_details2,self.order_details3],Promotion=self.promotion1)
        self.promotion2 = Promotion(promotion_id=2,threshold=100,decrease_sum=50,monthly_sum_limit=10000,monthly_sum_used=5000)
        self.order2 = Order(order_id=1, User=self.user1, order_details = [self.order_details1,self.order_details2,self.order_details3],Promotion=self.promotion2)
        self.promotion3 = Promotion(promotion_id=3,threshold=100,decrease_sum=50,monthly_sum_limit=10000,monthly_sum_used=9985)
        self.order3 = Order(order_id=1, User=self.user1, order_details = [self.order_details1,self.order_details2,self.order_details3],Promotion=self.promotion3)

        # 測試
        # 折扣為滿 100 折 30，全站每月折扣金額已達上限
        self.assertEqual(self.calc.calculate(self.order1),{'original_sum': 280, 'deduction': 0, 'deducted_sum': 280})
        # 折扣為滿 100 折 50，全站每月折扣金額未達上限(剩餘5000)
        self.assertEqual(self.calc.calculate(self.order2),{'original_sum': 280, 'deduction': 50, 'deducted_sum': 230})
        # 折扣為滿 100 折 50，全站每月折扣金額未達上限(剩餘15)
        self.assertEqual(self.calc.calculate(self.order3),{'original_sum': 280, 'deduction': 15, 'deducted_sum': 265})

    # 測試異常 promotion（不應該存在）
    def test_unexpected_promotion(self):
        self.promotion1 = Promotion(promotion_id=1,threshold=100,decrease_sum=30,monthly_sum_limit=10000,monthly_sum_used=10000,decrease_percentage=0.3,decrease_sum_limit=10)
        self.order1 = Order(order_id=1, User=self.user1, order_details = [self.order_details1,self.order_details2,self.order_details3],Promotion=self.promotion1)

        # 觸發 ValueError('Please contact customer service to inquire about this Order')
        with self.assertRaises(ValueError): 
            self.calc.calculate(self.order1)

if __name__ == "__main__":
    unittest.main()

    