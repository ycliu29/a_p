from logging import raiseExceptions
from abc import ABC, abstractmethod, abstractclassmethod

class User:
    def __init__(self, user_id: int):
        self.user_id = user_id

    def __str__(self):
        return 'User-{}'.format(self.user_id)

class Product:
    def __init__(self, product_id:int,product_unit_price:int):
        self.product_id = product_id
        self.product_unit_price = product_unit_price
    
    def __str__(self):
        return 'Product-{}'.format(self.product_id)

class Order:
    def __init__(self, order_id:int, order_details:dict):
        self.order_id = order_id
        # {Product(object):quantity,}
        self.order_details = order_details

    # 計算訂單未折扣金額
    def order_sum(self) -> int:
        order_sum = 0
        for key,value in self.order_details.items():
            order_sum += key.product_unit_price*value
        return order_sum

class Promotion:
    def __init__(self,promotion_id:int,threshold,discount):
        self.promotion_id = promotion_id
        self.threshold = threshold
        self.discount = discount

# 抽象折扣資格檢查類別
class Promo_Requirement_Checker(ABC):
    @abstractclassmethod
    def check(self, order:Order, promotion:Promotion) -> bool:
        pass

# 檢查 order 總額是否大於折扣門檻
class Order_sum_Promo_Requirement_Checker(Promo_Requirement_Checker):
    @classmethod
    def check(self, order:Order, promotion:Promotion) -> bool:
        return True if order.order_sum() >= promotion.threshold else False

# 檢查 order 中是否有單一品項大於折扣所需門檻
class Item_Amount_Promo_Requirement_Checker(Promo_Requirement_Checker):
    @classmethod
    def check(self, order:Order, promotion:Promotion) -> bool:
        for k,v in order.order_details.items():
            if k in promotion.threshold and v >= promotion.threshold[k]:
                return True
        return False

# 抽象折扣計算類別
class Promo_Deduction_Calculator(ABC):
    @abstractclassmethod
    def calculate_deduction(self, order:Order, promotion:Promotion):
        pass

class Percentage_Promo_Deduction_Calculator(Promo_Deduction_Calculator):
    @classmethod
    def calculate_deduction(self, order:Order, promotion:Promotion)-> int:
        # 無條件捨去
        deduction = int(order.order_sum() * promotion.discount)
        return deduction

class Sum_Promo_Deduction_Calculator(Promo_Deduction_Calculator):
    @classmethod
    def calculate_deduction(self, order:Order, promotion:Promotion)-> int:
        deduction = promotion.discount
        return deduction

class Calculator(ABC):
    @abstractclassmethod
    def calculate(cls,order:Order) -> dict:
        pass

# 用於折抵總價類促銷
class DiscountPromo_Calculator(Calculator):
    @classmethod
    def calculate(cls, order:Order, promotion:Promotion, promo_requirement:Promo_Requirement_Checker, promo_deduction:Promo_Deduction_Calculator) -> dict:
        pre_promotion_sum = order.order_sum()
        if promo_requirement.check(order, promotion) == True:
            deduction = promo_deduction.calculate_deduction(order,promotion)
        else:
            deduction = 0
        deducted_sum = pre_promotion_sum - deduction
        return_dict = {'pre_promotion_sum': pre_promotion_sum, 'deduction': deduction, 'deducted_sum': deducted_sum}
        return return_dict

class Nopromo_Calculator(Calculator):
    @classmethod
    def calculate(cls, order:Order) -> dict:
        pre_promotion_sum, deduction = order.order_sum(), 0
        deducted_sum = pre_promotion_sum
        return_dict = {'pre_promotion_sum': pre_promotion_sum, 'deduction': deduction, 'deducted_sum': deducted_sum}
        return return_dict
