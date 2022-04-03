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
    def __init__(self, order_id:int, order_details:dict[int:int]):
        self.order_id = order_id
        #[productID1:quantity,productID2:quantity...etc]
        self.order_details = order_details

    # 計算訂單未折扣金額
    def order_sum(self) -> int:
        order_sum = 0
        for key,value in self.order_details.items():
            order_sum += key.product_unit_price*value
        return order_sum

'''
class Calculator:
    def __init__(self) -> None:
        pass
    
    @classmethod
    def calculate(cls, Order):
        if Order.promotion == None:
            pre_promotion_sum = Order.order_sum()
            deduction = 0
            deducted_sum = pre_promotion_sum
            return_d = {'pre_promotion_sum': pre_promotion_sum, 'deduction': deduction, 'deducted_sum': deducted_sum}
            return return_d
        else: 
            pre_promotion_sum = Order.order_sum()
            deduction = Order.promotion.order_deduction()
            # check if deduction is int or a Product object
            if isinstance(deduction,Product):
                deducted_sum = pre_promotion_sum
            else:
                deducted_sum = pre_promotion_sum - deduction
            return_d = {'pre_promotion_sum': pre_promotion_sum, 'deduction': deduction, 'deducted_sum': deducted_sum}
            return return_d
'''