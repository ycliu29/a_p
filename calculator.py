class User:
    def __init__(self, user_id, user_email):
        # primary user id, set to none if not assigned
        self.user_id = user_id
        self.user_email = user_email
        return

class Product:
    def __init__(self, product_id,product_unit_price, manufacturer):
        self.product_id = product_id
        self.product_unit_price = product_unit_price
        self.product_manufacture = manufacturer
        return

class Order:
    def __init__(self, order_id, User, order_details, Promotion = None):
        self.order_id = order_id
        self.order_user= User
        # order_details will be passed in within a list
        self.order_details = order_details
        self.promotion = Promotion #default to None 
        return
    
    # return plain sum, not considering promotion
    def original_sum(self):
        original_sum = 0
        for item in self.order_details:
                original_sum = original_sum + item.product.product_unit_price * item.product_quantity
        if original_sum <= 0:
            raise ValueError('Order sum cannot be less than or equal to zero')
        return(original_sum)

class Order_Details:
    def __init__(self, order_details_id, order_id, Product, product_quantity):
        self.order_details_id = order_details_id
        self.order_id = order_id
        self.product = Product
        self.product_quantity = product_quantity

class Promotion:
    def __init__(self,promotion_id,limited_product=None,limited_product_threshold = None,threshold = None,decrease_sum=None,decrease_percentage = None,free_item = None,usage_count_limit = None,usage_used_count = None,decrease_sum_limit = None,promotion_sum_limit = None,promotion_sum_used = None):
        self.id = promotion_id
        # when order sum(limits to certain product if specified) >= threshold, the promotion will be triggered
        self.limited_product = limited_product #pass in one Product
        self.limited_product_threshold = limited_product_threshold # pass in integer, promotion will be triggered once order has >= threhold amounts of limited product
        self.threshold = threshold 
        # promotion types
        self.decrease_sum = decrease_sum # integer only
        self.decrease_percentage = decrease_percentage
        self.free_item = free_item #pass in Product
        # promotion constraints
        self.usage_count_limit = usage_count_limit
        self.usage_used_count = usage_used_count
        self.decrease_sum_limit = decrease_sum_limit
        self.promotion_sum_limit = promotion_sum_limit
        self.promotion_sum_used = promotion_sum_used

# return dictionary with the following keys(original_sum, deduction, deducted_sum)
# logic: check if there's promotion -> if it's by certain product count -> if promotion threshold is met -> if there's prmotion limit -> apply promotion
class Calculator:
    def __init__(self):
        self.version = 1.0
    
    def calculate(self,Order):
        original_sum, deduction, deducted_sum = 0, 0, 0
        # 基礎案例 無 promotion
        if Order.promotion == None:
            original_sum = Order.original_sum()
            # no promotion used thus having the same original, deducted sum
            deducted_sum = original_sum
            return_d = {'original_sum': original_sum, 'deduction': deduction, 'deducted_sum': deducted_sum}
            return return_d
        
        else:
            # 檢查 promotion 是否以特定產品數量作為判定條件
            if Order.promotion.limited_product != None:
                meet_requirement = False
                # iterate order_details 中的 order_detail, 確認訂單是否符合 Promotion 的數量條件
                for item in Order.order_details:
                    if item.product == Order.promotion.limited_product:
                        if item.product_quantity >= Order.promotion.limited_product_threshold: meet_requirement = True
                # 商品數量未達門檻，不使用 promotion 結算
                if meet_requirement == False:
                    original_sum = Order.original_sum()
                    deducted_sum = original_sum
                    return_d = {'original_sum': original_sum, 'deduction': deduction, 'deducted_sum': deducted_sum}
                    return return_d
                else: 
                    original_sum = Order.original_sum()
                    deduction = Order.promotion.decrease_sum
                    deducted_sum = original_sum - deduction
                    if deducted_sum <= 0:
                        raise ValueError('Order sum cannot be less than or equal to zero')
                    return_d = {'original_sum': original_sum, 'deduction': deduction, 'deducted_sum': deducted_sum}
                    return return_d

            # 檢查訂單是否滿 x 元 Promotion.threshold
            else:
                # 訂單金額不足以使用 Promotion
                if Order.original_sum() < int(Order.promotion.threshold):
                    original_sum = Order.original_sum()
                    deducted_sum = original_sum
                    return_d = {'original_sum': original_sum, 'deduction': deduction, 'deducted_sum': deducted_sum}
                    return return_d
                # 訂單金額已觸發 Promotion
                # 檢測觸發種類 | 同時只能觸發一種（free_item, decrease_sum, decrease_percentage)
                else: 
                    # 觸發 free_item
                    if Order.promotion.free_item != None and Order.promotion.decrease_sum == None and Order.promotion.decrease_percentage == None:
                        original_sum = Order.original_sum()
                        deduction = 'free_product_id: ' + str(Order.promotion.free_item.product_id)
                        deducted_sum = original_sum
                        return_d = {'original_sum': original_sum, 'deduction': deduction, 'deducted_sum': deducted_sum}
                        return return_d
                    
                    # 觸發 decrease_percentage
                    elif Order.promotion.free_item == None and Order.promotion.decrease_sum == None and Order.promotion.decrease_percentage != None:
                        # 檢測是否有優惠上限
                        # 無優惠 n 元上限
                        if Order.promotion.decrease_sum_limit == None:
                            original_sum = Order.original_sum()
                            deduction = int(original_sum * Order.promotion.decrease_percentage) # int() 無條件捨去小數點
                            deducted_sum = original_sum - deduction
                            return_d = {'original_sum': original_sum, 'deduction': deduction, 'deducted_sum': deducted_sum}
                            return return_d
                        # 有優惠 n 元上限
                        else:
                            # TODO
                            pass






