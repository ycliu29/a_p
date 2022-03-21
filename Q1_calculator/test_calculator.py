import unittest
from calculator import User, Product, Order, Calculator
from promotion import Promotion, Promotion_free_item, Promotion_item_threshold, Promotion_usage_count_limit
 
class TestOrderClass(unittest.TestCase):
    def setUp(self):
        self.user1 = User(user_id = 1)
        self.product1 = Product(product_id=1,product_unit_price=30)
        self.product2 = Product(product_id=2,product_unit_price=20)
        self.order1 = Order(order_id=1,User=self.user1,order_details={self.product1:3,self.product2:5})
    
    # 測試 order_sum 能正確回傳訂單總金額
    def test_order_sum(self):
        self.assertEqual(self.order1.order_sum(),190)

class TestPromotionClass(unittest.TestCase):
    def setUp(self):
        self.user1 = User(user_id = 1)
        self.product1 = Product(product_id=1,product_unit_price=30)
        self.product2 = Product(product_id=2,product_unit_price=20)
        self.order1 = Order(order_id=1,User=self.user1,order_details={self.product1:3,self.product2:5})
    
    def test_meet_promotion_requirement(self):
        self.promotion1 = Promotion(promotion_id=1,Order=self.order1,threshold=189,discount=50)
        self.promotion2 = Promotion(promotion_id=2,Order=self.order1,threshold=190,discount=50)
        self.promotion3 = Promotion(promotion_id=3,Order=self.order1,threshold=191,discount=50)

        # 測試方法能正確回傳是否達到折扣標準
        self.assertEqual(self.promotion1.meet_promotion_requirement(),True)
        self.assertEqual(self.promotion2.meet_promotion_requirement(),True)
        self.assertEqual(self.promotion3.meet_promotion_requirement(),False)
    
    def test_calc_deduction(self):
        self.promotion1 = Promotion(promotion_id=1,Order=self.order1,threshold=190,discount=0.07)
        self.promotion2 = Promotion(promotion_id=2,Order=self.order1,threshold=190,discount=0.1)
        self.promotion3 = Promotion(promotion_id=3,Order=self.order1,threshold=190,discount=30)
        self.promotion4 = Promotion(promotion_id=4,Order=self.order1,threshold=190,discount=-50)

        # 測試方法能正確回傳折扣值並處理小數點（捨去），無定義情形時報錯
        self.assertEqual(self.promotion1.calc_deduction(),13)
        self.assertEqual(self.promotion2.calc_deduction(),19)
        self.assertEqual(self.promotion3.calc_deduction(),30)
        with self.assertRaises(ValueError): 
            self.promotion4.calc_deduction()

    def test_order_deduction(self):
        self.promotion1 = Promotion(promotion_id=1,Order=self.order1,threshold=190,discount=0.1)
        self.promotion2 = Promotion(promotion_id=2,Order=self.order1,threshold=191,discount=0.1)

        # 測試方法能正確呼叫 meet_promotion_requirement, order_deduction 兩方法並回傳折扣值
        self.assertEqual(self.promotion1.order_deduction(),19)
        self.assertEqual(self.promotion2.order_deduction(),0)

class TestPromotion_free_itemClass(unittest.TestCase):
    def setUp(self):
        self.user1 = User(user_id = 1)
        self.product1 = Product(product_id=1,product_unit_price=30)
        self.product2 = Product(product_id=2,product_unit_price=20)
        self.order1 = Order(order_id=1,User=self.user1,order_details={self.product1:3,self.product2:5},Promotion=None)
    
    def test_calc_deduction(self):
        # Promotion 為滿 190 元贈送 product1
        self.promotion_free_item1 = Promotion_free_item(promotion_id=1,Order=self.order1,threshold=190,discount=self.product1)
        self.order1.Promotion=self.promotion_free_item1

        self.assertEqual(self.promotion_free_item1.calc_deduction(),self.product1)

class TestPromotion_item_thresholdClass(unittest.TestCase):
    def setUp(self):
        self.user1 = User(user_id = 1)
        self.product1 = Product(product_id=1,product_unit_price=30)
        self.product2 = Product(product_id=2,product_unit_price=20)
        self.order1 = Order(order_id=1,User=self.user1,order_details={self.product1:3,self.product2:5},Promotion=None)
    
    def test_meet_promotion_requirement(self):
        # 測試資格確認功能
        self.promotion_item_threshold1 = Promotion_item_threshold(promotion_id=1,Order=self.order1,threshold=3,discount=30,item_list=[self.product1])
        self.promotion_item_threshold2 = Promotion_item_threshold(promotion_id=2,Order=self.order1,threshold=10,discount=30,item_list=[self.product1])

        # 折扣一門檻為 3 個，訂單為 8，故 True｜折扣二門檻為 10，訂單為 8，故 False
        self.assertEqual(self.promotion_item_threshold1.meet_promotion_requirement(),True)
        self.assertEqual(self.promotion_item_threshold2.meet_promotion_requirement(),False)

class TestPromotion_usage_count_limitClass(unittest.TestCase):
    def setUp(self):
        self.user1 = User(user_id = 1)
        self.product1 = Product(product_id=1,product_unit_price=30)
        self.product2 = Product(product_id=2,product_unit_price=20)
        self.order1 = Order(order_id=1,User=self.user1,order_details={self.product1:3,self.product2:5},Promotion=None)

    def test_meet_promotion_requirement(self):
        # 測試資格確認功能
        self.promotion_usage_count_limit1 = Promotion_usage_count_limit(promotion_id=1,Order=self.order1,threshold=150,discount=30,current_usage=10,usage_limit=100)
        self.promotion_usage_count_limit2 = Promotion_usage_count_limit(promotion_id=2,Order=self.order1,threshold=150,discount=30,current_usage=100,usage_limit=100)

        self.assertEqual(self.self.promotion_usage_count_limit1.meet_promotion_requirement(),True)
        self.assertEqual(self.self.promotion_usage_count_limit2.meet_promotion_requirement(),False)

class TestCalculatorClass(unittest.TestCase):
    def setUp(self):
        self.user1 = User(user_id = 1)
        self.product1 = Product(product_id=1,product_unit_price=30)
        self.product2 = Product(product_id=2,product_unit_price=20)
        self.order1 = Order(order_id=1,User=self.user1,order_details={self.product1:3,self.product2:5})
        self.promotion1 = Promotion(promotion_id=1,Order=self.order1,threshold=190,discount=0.1)
        self.promotion2 = Promotion_free_item(promotion_id=2,Order=self.order1,threshold=190,discount=self.product1)
        self.promotion3 = Promotion_item_threshold(promotion_id=3,Order=self.order1,threshold=3,discount=30, item_list=[self.product1])
        self.promotion4 = Promotion_item_threshold(promotion_id=4,Order=self.order1,threshold=10,discount=30, item_list=[self.product1])
        
    def test_calculate(self):
        self.calc1 = Calculator()
        self.order2 = Order(order_id=2,User=self.user1,order_details={self.product1:3,self.product2:5}, Promotion=self.promotion1)
        self.order3 = Order(order_id=3,User=self.user1,order_details={self.product1:3,self.product2:5}, Promotion=self.promotion2)
        self.order4 = Order(order_id=4,User=self.user1,order_details={self.product1:3,self.product2:5}, Promotion=self.promotion3)
        self.order5 = Order(order_id=5,User=self.user1,order_details={self.product1:3,self.product2:5}, Promotion=self.promotion4)
        
        # 測試 calculate，Order 無 promotion
        self.assertEqual(self.calc1.calculate(self.order1),{'pre_promotion_sum': 190, 'deduction': 0, 'deducted_sum': 190})
        # 測試 calculate，Promotion 為訂單滿 190 減免 10%
        self.assertEqual(self.calc1.calculate(self.order2),{'pre_promotion_sum': 190, 'deduction': 19, 'deducted_sum': 171})
        # 測試 calculate，Promotion 為訂單滿 190 贈送 product1
        self.assertEqual(self.calc1.calculate(self.order3),{'pre_promotion_sum': 190, 'deduction': self.product1, 'deducted_sum': 190})
        # 測試 calculate，Promotion 為 Product1 滿 3 個 折 30 元
        self.assertEqual(self.calc1.calculate(self.order4),{'pre_promotion_sum': 190, 'deduction': 30, 'deducted_sum': 160})
        # 測試 calculate，Promotion 為 Product1 滿 10 個 折 30 元（未觸發）
        self.assertEqual(self.calc1.calculate(self.order5),{'pre_promotion_sum': 190, 'deduction': 0, 'deducted_sum': 190})

if __name__ == "__main__":
    unittest.main()
