import unittest
from calculator import User, Product, Order, Promotion, Promotion_usage_limit, Promotion_per_order_limit, Promotion_site_usage_sum_limit, Promo_Requirement_Checker, Order_sum_Promo_Requirement_Checker, Item_Amount_Promo_Requirement_Checker, Order_sum_usage_limit_Promo_Requirement_Checker, Promo_Deduction_Calculator, Percentage_Promo_Deduction_Calculator, Percentage_withlimit_Promo_Deduction_Calculator, Sum_Promo_Deduction_Calculator, Sum_site_limit_Promo_Deduction_Calculator, FreeItem_Promo_Deduction_Calculator, DiscountPromo_Calculator,  Nopromo_Calculator, FixedDiscountPromo_Calculator, FreeItem_Promo_Calculator

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

class TestOrder_sum_usage_limit_Promo_Requirement_Checker(unittest.TestCase):
    def setUp(self):
        self.product1 = Product(product_id=1,product_unit_price=100)
        self.order1 = Order(order_id=1,order_details={self.product1:5})
        self.promotion1 = Promotion_usage_limit(promotion_id=1,threshold=300,discount=50,usage_limit=10,current_usage=5)
        self.promotion2 = Promotion_usage_limit(promotion_id=2,threshold=300,discount=50,usage_limit=5,current_usage=5)

    def test_check(self):
        self.assertEqual(Order_sum_usage_limit_Promo_Requirement_Checker.check(self.order1,self.promotion1),True)
        self.assertEqual(Order_sum_usage_limit_Promo_Requirement_Checker.check(self.order1,self.promotion2),False)

class TestPercentage_Promo_Deduction_Calculator(unittest.TestCase):
    def setUp(self):
        self.product1 = Product(product_id=1,product_unit_price=70)
        self.order1 = Order(order_id=1,order_details={self.product1:8})
        self.promotion1 = Promotion(promotion_id=1,threshold=500,discount=0.1)
        self.promotion2 = Promotion(promotion_id=2,threshold=500,discount=0.07)
    
    def test_calculate_deduction(self):
        self.assertEqual(Percentage_Promo_Deduction_Calculator.calculate_deduction(self.order1,self.promotion1),56)
        self.assertEqual(Percentage_Promo_Deduction_Calculator.calculate_deduction(self.order1,self.promotion2),39)

class TestPercentage_withlimit_Promo_Deduction_Calculator(unittest.TestCase):
    def setUp(self):
        self.product1 = Product(product_id=1,product_unit_price=70)
        self.order1 = Order(order_id=1,order_details={self.product1:8})
        self.promotion1 = Promotion_per_order_limit(promotion_id=1,threshold=500,discount=0.1, per_order_limit=50)
        self.promotion2 = Promotion_per_order_limit(promotion_id=1,threshold=500,discount=0.1, per_order_limit=80)
    
    def test_calculate_deduction(self):
        self.assertEqual(Percentage_withlimit_Promo_Deduction_Calculator.calculate_deduction(self.order1,self.promotion1),50)
        self.assertEqual(Percentage_withlimit_Promo_Deduction_Calculator.calculate_deduction(self.order1,self.promotion2),56)

class TestFreeItem_Promo_Deduction_Calculator(unittest.TestCase):
    def setUp(self):
        self.product1 = Product(product_id=1,product_unit_price=70)
        self.promotion1 = Promotion(promotion_id=1,threshold=500,discount=self.product1)
    
    def test_calculate_deduction(self):
        self.assertEqual(FreeItem_Promo_Deduction_Calculator.calculate_deduction(self.promotion1),self.product1)

class TestSum_Promo_Deduction_Calculator(unittest.TestCase):
    def setUp(self):
        self.promotion1 = Promotion(promotion_id=1,threshold=500,discount=30)
    
    def test_calculate_deduction(self):
        self.assertEqual(Sum_Promo_Deduction_Calculator.calculate_deduction(self.promotion1),30)

class TestSum_site_limit_Promo_Deduction_Calculator(unittest.TestCase):
    def setUp(self):
        self.promotion1 = Promotion_site_usage_sum_limit(promotion_id=1,threshold=500,discount=30,usage_limit=500,current_usage=30)
        self.promotion2 = Promotion_site_usage_sum_limit(promotion_id=2,threshold=500,discount=30,usage_limit=500,current_usage=500)
        self.promotion3 = Promotion_site_usage_sum_limit(promotion_id=3,threshold=500,discount=30,usage_limit=500,current_usage=490)
    
    def test_calculate_deduction(self):
        self.assertEqual(Sum_site_limit_Promo_Deduction_Calculator.calculate_deduction(self.promotion1),30)
        self.assertEqual(Sum_site_limit_Promo_Deduction_Calculator.calculate_deduction(self.promotion2),0)
        self.assertEqual(Sum_site_limit_Promo_Deduction_Calculator.calculate_deduction(self.promotion3),10)

class TestNopromo_CalculatorClass(unittest.TestCase):
    def setUp(self):
        self.product1 = Product(product_id=1,product_unit_price=10)
        self.product2 = Product(product_id=2, product_unit_price=20)
        self.order1 = Order(order_id=1,order_details={self.product1:5,self.product2:10})

    def test_calculate(self):
        self.assertEqual(Nopromo_Calculator.calculate(self.order1),{'pre_promotion_sum': 250, 'deduction': 0, 'deducted_sum': 250})

# 整合測試
# 測試場景：訂單滿 X 元折 Z % | 滿 X 元折 Z %，折扣每⼈只能總共優惠 N 元
class TestDiscountPromo_Calculator(unittest.TestCase):
    def setUp(self):
        self.product1 = Product(product_id=1,product_unit_price=10)
        self.product2 = Product(product_id=2, product_unit_price=20)
        self.order1 = Order(order_id=1,order_details={self.product1:5,self.product2:10})
        self.promotion1 = Promotion(promotion_id=1,threshold=200,discount=0.1)
        self.promotion2 = Promotion_per_order_limit(promotion_id=2,threshold=200,discount=0.1,per_order_limit=20)
        self.promotion3 = Promotion_per_order_limit(promotion_id=3,threshold=200,discount=0.1,per_order_limit=50)
    
    def test_calculate(self):
        # 訂單滿 X 元折 Z %
        self.assertEqual(DiscountPromo_Calculator.calculate(self.order1,self.promotion1,Order_sum_Promo_Requirement_Checker,Percentage_Promo_Deduction_Calculator),{'pre_promotion_sum': 250, 'deduction': 25, 'deducted_sum': 225})

        # 滿 X 元折 Z %，折扣每⼈只能總共優惠 N 元
        self.assertEqual(DiscountPromo_Calculator.calculate(self.order1,self.promotion2,Order_sum_Promo_Requirement_Checker,Percentage_withlimit_Promo_Deduction_Calculator),{'pre_promotion_sum': 250, 'deduction': 20, 'deducted_sum': 230})
        self.assertEqual(DiscountPromo_Calculator.calculate(self.order1,self.promotion3,Order_sum_Promo_Requirement_Checker,Percentage_withlimit_Promo_Deduction_Calculator),{'pre_promotion_sum': 250, 'deduction': 25, 'deducted_sum': 225})

# 測試場景：特定商品滿 X 件折 Y 元 | 滿 X 元折 Y 元，在全站總共只能套⽤ N 次 | 滿 X 元折 Y 元，全站折扣上限為 N 元
class TestFixedDiscountPromo_Calculator(unittest.TestCase):
    def setUp(self):
        self.product1 = Product(product_id=1,product_unit_price=10)
        self.product2 = Product(product_id=2, product_unit_price=20)
        self.order1 = Order(order_id=1,order_details={self.product1:5,self.product2:10})
        self.promotion1 = Promotion(promotion_id=1,threshold={self.product1:5},discount=30)
        self.promotion2 = Promotion_usage_limit(promotion_id=2,threshold=200,discount=20,usage_limit=5,current_usage=3)
        self.promotion3 = Promotion_usage_limit(promotion_id=3,threshold=200,discount=20,usage_limit=5,current_usage=5)
        self.promotion4 = Promotion_site_usage_sum_limit(promotion_id=4,threshold=200,discount=30,usage_limit=300,current_usage=20)
        self.promotion5 = Promotion_site_usage_sum_limit(promotion_id=5,threshold=200,discount=30,usage_limit=300,current_usage=290)
        self.promotion6 = Promotion_site_usage_sum_limit(promotion_id=6,threshold=200,discount=30,usage_limit=300,current_usage=310)
    
    def test_calculate(self):
        # 特定商品滿 X 件折 Y 元
        self.assertEqual(FixedDiscountPromo_Calculator.calculate(self.order1,self.promotion1,Item_Amount_Promo_Requirement_Checker,Sum_Promo_Deduction_Calculator),{'pre_promotion_sum': 250, 'deduction': 30, 'deducted_sum': 220})
        # 滿 X 元折 Y 元，在全站總共只能套⽤ N 次
        self.assertEqual(FixedDiscountPromo_Calculator.calculate(self.order1,self.promotion2,Order_sum_usage_limit_Promo_Requirement_Checker,Sum_Promo_Deduction_Calculator),{'pre_promotion_sum': 250, 'deduction': 20, 'deducted_sum': 230})
        self.assertEqual(FixedDiscountPromo_Calculator.calculate(self.order1,self.promotion3,Order_sum_usage_limit_Promo_Requirement_Checker,Sum_Promo_Deduction_Calculator),{'pre_promotion_sum': 250, 'deduction': 0, 'deducted_sum': 250})

        # 滿 X 元折 Y 元，全站折扣上限為 N 元
        self.assertEqual(FixedDiscountPromo_Calculator.calculate(self.order1,self.promotion4,Order_sum_usage_limit_Promo_Requirement_Checker,Sum_site_limit_Promo_Deduction_Calculator),{'pre_promotion_sum': 250, 'deduction': 30, 'deducted_sum': 220})
        self.assertEqual(FixedDiscountPromo_Calculator.calculate(self.order1,self.promotion5,Order_sum_usage_limit_Promo_Requirement_Checker,Sum_site_limit_Promo_Deduction_Calculator),{'pre_promotion_sum': 250, 'deduction': 10, 'deducted_sum': 240})
        self.assertEqual(FixedDiscountPromo_Calculator.calculate(self.order1,self.promotion6,Order_sum_usage_limit_Promo_Requirement_Checker,Sum_site_limit_Promo_Deduction_Calculator),{'pre_promotion_sum': 250, 'deduction': 0, 'deducted_sum': 250})

# 測試場景：訂單滿 X 元贈送特定商品
class TestFreeItem_Promo_Calculator(unittest.TestCase):
    def setUp(self):
        self.product1 = Product(product_id=1,product_unit_price=10)
        self.product2 = Product(product_id=2, product_unit_price=20)
        self.order1 = Order(order_id=1,order_details={self.product1:5,self.product2:10})
        self.promotion1 = Promotion(promotion_id=1,threshold=200,discount=self.product1)

    def test_calculate(self):
        # 訂單滿 X 元贈送特定商品
        self.assertEqual(FreeItem_Promo_Calculator.calculate(self.order1,self.promotion1,Order_sum_Promo_Requirement_Checker,FreeItem_Promo_Deduction_Calculator),{'pre_promotion_sum': 250, 'deduction': self.product1, 'deducted_sum': 250})

if __name__ == "__main__":
    unittest.main()