import unittest
from calculator import DiscountPromo_Calculator
from calculator import User, Product, Order, Promotion, Promo_Requirement_Checker, Order_sum_Promo_Requirement_Checker, Item_Amount_Promo_Requirement_Checker,Promo_Deduction_Calculator, Percentage_Promo_Deduction_Calculator, Sum_Promo_Deduction_Calculator, Nopromo_Calculator

# 單元測試
class TestOrderClass(unittest.TestCase):
    def setUp(self):
        self.product1 = Product(product_id=1,product_unit_price=10)
        self.product2 = Product(product_id=2, product_unit_price=20)
        self.order1 = Order(order_id=1,order_details={self.product1:5,self.product2:10})

    def test_order_sum(self):
        self.assertEqual(self.order1.order_sum(),250)

class TestOrder_sum_Promo_Requirement_Checker(unittest.TestCase):
    def setUp(self):
        self.product1 = Product(product_id=1,product_unit_price=100)
        self.order1 = Order(order_id=1,order_details={self.product1:5})
        self.promotion1 = Promotion(promotion_id=1,threshold=500,discount=50)
        self.promotion2 = Promotion(promotion_id=2,threshold=600,discount=50)
    
    def test_check(self):
        self.assertEqual(Order_sum_Promo_Requirement_Checker.check(self.order1,self.promotion1),True)
        self.assertEqual(Order_sum_Promo_Requirement_Checker.check(self.order1,self.promotion2),False)

class TestItem_Amount_Promo_Requirement_Checker(unittest.TestCase):
    def setUp(self):
        self.product1 = Product(product_id=1,product_unit_price=100)
        self.product2 = Product(product_id=2,product_unit_price=50)
        self.order1 = Order(order_id=1,order_details={self.product1:5})
        self.promotion1 = Promotion(promotion_id=1,threshold={self.product1:5},discount=50)
        self.promotion2 = Promotion(promotion_id=2,threshold={self.product1:6,self.product2:3},discount=50)

    def test_check(self):
        self.assertEqual(Item_Amount_Promo_Requirement_Checker.check(self.order1,self.promotion1),True)
        self.assertEqual(Item_Amount_Promo_Requirement_Checker.check(self.order1,self.promotion2),False)

class TestPercentage_Promo_Deduction_Calculator(unittest.TestCase):
    def setUp(self):
        self.product1 = Product(product_id=1,product_unit_price=70)
        self.order1 = Order(order_id=1,order_details={self.product1:8})
        self.promotion1 = Promotion(promotion_id=1,threshold=500,discount=0.1)
        self.promotion2 = Promotion(promotion_id=2,threshold=500,discount=0.07)
    
    def test_calculate_deduction(self):
        self.assertEqual(Percentage_Promo_Deduction_Calculator.calculate_deduction(self.order1,self.promotion1),56)
        self.assertEqual(Percentage_Promo_Deduction_Calculator.calculate_deduction(self.order1,self.promotion2),39)

class TestSum_Promo_Deduction_Calculator(unittest.TestCase):
    def setUp(self):
        self.product1 = Product(product_id=1,product_unit_price=70)
        self.order1 = Order(order_id=1,order_details={self.product1:8})
        self.promotion1 = Promotion(promotion_id=1,threshold=500,discount=30)
    
    def test_calculate_deduction(self):
        self.assertEqual(Sum_Promo_Deduction_Calculator.calculate_deduction(self.order1, self.promotion1),30)

class TestNopromo_CalculatorClass(unittest.TestCase):
    def setUp(self):
        self.product1 = Product(product_id=1,product_unit_price=10)
        self.product2 = Product(product_id=2, product_unit_price=20)
        self.order1 = Order(order_id=1,order_details={self.product1:5,self.product2:10})

    def test_calculate(self):
        self.assertEqual(Nopromo_Calculator.calculate(self.order1),{'pre_promotion_sum': 250, 'deduction': 0, 'deducted_sum': 250})

# 整合測試
class TestDiscountPromo_Calculator(unittest.TestCase):
    def setUp(self):
        self.product1 = Product(product_id=1,product_unit_price=10)
        self.product2 = Product(product_id=2, product_unit_price=20)
        self.order1 = Order(order_id=1,order_details={self.product1:5,self.product2:10})
        self.promotion1 = Promotion(promotion_id=1,threshold=200,discount=0.1)
        self.promotion2 = Promotion(promotion_id=2,threshold={self.product1:5},discount=30)
    
    def test_calculate(self):
        # 訂單滿 X 元折 Z %
        self.assertEqual(DiscountPromo_Calculator.calculate(self.order1,self.promotion1,Order_sum_Promo_Requirement_Checker,Percentage_Promo_Deduction_Calculator),{'pre_promotion_sum': 250, 'deduction': 25, 'deducted_sum': 225})

        # 特定商品滿 X 件折 Y 元
        self.assertEqual(DiscountPromo_Calculator.calculate(self.order1,self.promotion2,Item_Amount_Promo_Requirement_Checker,Sum_Promo_Deduction_Calculator),{'pre_promotion_sum': 250, 'deduction': 30, 'deducted_sum': 220})

if __name__ == "__main__":
    unittest.main()