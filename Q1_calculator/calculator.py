from logging import raiseExceptions


class User:
    def __init__(self, user_id, user_email):
        # 基礎 user 資訊
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
        # order_details 以 list 形式儲存
        self.order_details = order_details
        self.promotion = Promotion #default to None 
        return
    
    # 計算折扣前訂單總額
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
    def __init__(self,promotion_id,limited_product=None,limited_product_threshold = None,threshold = None,decrease_sum=None,decrease_percentage = None,free_item = None,usage_count_limit = None,usage_used_count = None,decrease_sum_limit = None,monthly_sum_limit = None,monthly_sum_used = None):
        self.id = promotion_id
        # 傳入一 Product 類別物件，可以改為 list of Product objects, 視業務單位需求定義
        self.limited_product = limited_product
        # 傳入一正整數，當訂單內 Product 數量 >= limited_product_threshold，觸發優惠
        self.limited_product_threshold = limited_product_threshold 
        # 如 threshold 存在，當折扣前訂單總額大於等於 threshold，觸發 promotion
        self.threshold = threshold 
        # 優惠種類
        # 傳入要扣抵的金額（正整數）
        self.decrease_sum = decrease_sum 
        # 傳入要扣抵的百分比（正整數），若折扣金額產生小數點，無條件捨去，可以透過 decrease_sum_limit 設定單筆折扣折抵金額上限（正整數）
        self.decrease_percentage = decrease_percentage
        self.decrease_sum_limit = decrease_sum_limit
        # 傳入（贈品）Product object
        self.free_item = free_item
        # promotion 限制
        # 使用次數上限及已使用次數
        self.usage_count_limit = usage_count_limit
        self.usage_used_count = usage_used_count
        # 每月折扣額度上限及已折扣額度
        self.monthly_sum_limit = monthly_sum_limit
        self.monthly_sum_used = monthly_sum_used

# Calculator 完成計算後回傳一有下列三 key(original_sum, deduction, deducted_sum)的 dictionary
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
            if Order.promotion.limited_product != None and Order.promotion.threshold==None:
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
            elif Order.promotion.limited_product == None and Order.promotion.threshold!=None:
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
                            original_sum = Order.original_sum()
                            deduction = int(original_sum * Order.promotion.decrease_percentage) # int() 無條件捨去小數點
                            # 確保優惠金額 <= 上限
                            if deduction > Order.promotion.decrease_sum_limit:
                                deduction = Order.promotion.decrease_sum_limit
                            deducted_sum = original_sum - deduction
                            return_d = {'original_sum': original_sum, 'deduction': deduction, 'deducted_sum': deducted_sum}
                            return return_d
                    
                    # 觸發 decrease_sum
                    elif Order.promotion.free_item == None and Order.promotion.decrease_sum != None and Order.promotion.decrease_percentage == None:
                        # 檢測 promotion 屬於折扣次數上限或每月折扣金額上限
                        # 折扣次數上限
                        if Order.promotion.usage_count_limit != None and Order.promotion.usage_used_count != None and Order.promotion.monthly_sum_used == None and Order.promotion.monthly_sum_limit == None:
                            # 檢測折扣使用次數是否已達上限
                            # 折扣使用次數已等於或大於上限
                            if Order.promotion.usage_count_limit <= Order.promotion.usage_used_count: 
                                original_sum = Order.original_sum()
                                deducted_sum = original_sum
                                return_d = {'original_sum': original_sum, 'deduction': deduction, 'deducted_sum': deducted_sum}
                                return return_d
                            # 折扣使用次數未達上限
                            else:
                                original_sum = Order.original_sum()
                                deduction = Order.promotion.decrease_sum
                                deducted_sum = original_sum - deduction
                                return_d = {'original_sum': original_sum, 'deduction': deduction, 'deducted_sum': deducted_sum}
                                return return_d
                        # 每月折扣金額上限
                        elif Order.promotion.usage_count_limit == None and Order.promotion.usage_used_count == None and Order.promotion.monthly_sum_used != None and Order.promotion.monthly_sum_limit != None:
                            # 折扣已使用等於或超過每月折扣上限
                            if Order.promotion.monthly_sum_used >= Order.promotion.monthly_sum_limit:
                                original_sum = Order.original_sum()
                                deducted_sum = original_sum
                                return_d = {'original_sum': original_sum, 'deduction': deduction, 'deducted_sum': deducted_sum}
                                return return_d
                            # 折扣使用小於本月額度，且單筆折扣金額小於等於剩餘額度
                            elif Order.promotion.monthly_sum_used < Order.promotion.monthly_sum_limit and Order.promotion.monthly_sum_limit-Order.promotion.monthly_sum_used >= Order.promotion.decrease_sum:
                                original_sum = Order.original_sum()
                                deduction = Order.promotion.decrease_sum
                                deducted_sum = original_sum - deduction
                                return_d = {'original_sum': original_sum, 'deduction': deduction, 'deducted_sum': deducted_sum}
                                return return_d

                            # 折扣使用小於本月額度，但單筆折扣金額大於剩餘額度
                            elif Order.promotion.monthly_sum_used < Order.promotion.monthly_sum_limit and Order.promotion.monthly_sum_limit-Order.promotion.monthly_sum_used < Order.promotion.decrease_sum:
                                original_sum = Order.original_sum()
                                deduction = Order.promotion.monthly_sum_limit-Order.promotion.monthly_sum_used
                                deducted_sum = original_sum - deduction
                                return_d = {'original_sum': original_sum, 'deduction': deduction, 'deducted_sum': deducted_sum}
                                return return_d
                    
        # 如有未定義案例(promotion)，顯示錯誤
        raise ValueError('Please contact customer service to inquire about this Order')
                
            
            