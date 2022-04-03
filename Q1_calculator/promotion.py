from logging import raiseExceptions
import calculator

# 基礎 Promotion 類別，適用於訂單滿 X 元折 Z% | 訂單滿 X 元折 Y 元
class Promotion:
    def __init__(self,promotion_id,Order,threshold,discount):
        self.promotion_id = promotion_id
        self.Order = Order
        self.threshold = threshold
        self.discount = discount
    
    # 確認訂單是否符合 promotion 資格
    def meet_promotion_requirement(self):
        if self.Order.order_sum() >= self.threshold: 
            return True
        else: 
            return False

    # 計算折扣金額
    def calc_deduction(self):
        # deduction 為折扣百分比，小數點無條件捨去
        if self.discount > 0 and self.discount < 1:
            return int(self.discount * self.Order.order_sum())
        # deduction 為折扣 y 元
        elif self.discount > 1:
            return self.discount
        # 未定義情況將報 ValueError
        else:
            raise ValueError('Please check promotion discount setting')
        
    # return 折扣金額或 0（不符合 promotion 資格）
    def order_deduction(self):
        if self.meet_promotion_requirement() == True:
            return self.calc_deduction()
        else:
            return 0

# 繼承 Promotion 類別，適用於訂單滿 X 元送特定商品(於 discount 傳入贈品 Product object)
class Promotion_free_item(Promotion):
    def __init__(self, promotion_id, Order, threshold, discount):
        super().__init__(promotion_id, Order, threshold, discount)
    
    # 修改 discount 折扣內容
    def calc_deduction(self):
        if isinstance(self.discount,calculator.Product):
            return self.discount
        # 未定義情況將報 ValueError
        else:
            raise ValueError('Please check promotion discount setting')

# 繼承 Promotion 類別，適用於訂單有特定商品 x 件，折 y 元或 z%，
class Promotion_item_threshold(Promotion):
    def __init__(self, promotion_id, Order, threshold, discount, item_list):
        super().__init__(promotion_id, Order, threshold, discount)
        self.item_list = item_list # 傳入一 list of Product objects，若有多件 Prdouct, 數量會共同加總計算
    
    # 修改資格確認方式（金額改為產品數量）
    def meet_promotion_requirement(self):
        count = 0
        for item in self.item_list:
            if item in self.Order.order_details:
                count += self.Order.order_details[item]
        if count >= self.threshold:
            return True
        else: 
            return False

# 繼承 Promotion 類別，適用於訂單滿 x 元折 y%  or z 元，全站總共只能套⽤ N 次
class Promotion_usage_count_limit(Promotion):
    def __init__(self, promotion_id, Order, threshold, discount,current_usage,usage_limit):
        super().__init__(promotion_id, Order, threshold, discount)
        self.current_usage = current_usage
        self.usage_limit = usage_limit
    
    # 修改資格確認方式（加入使用次數驗證）
    def meet_promotion_requirement(self):
        if self.Order.order_sum() >= self.threshold and self.usage_limit>self.current_usage: 
            return True
        else: 
            return False

# 繼承 Promotion 類別，適用於訂單滿 x 元折 y%  or z 元，限制每訂單（人）折扣上限
class Promotion_deduction_limit(Promotion):
    def __init__(self, promotion_id, Order, threshold, discount,discount_limit):
        super().__init__(promotion_id, Order, threshold, discount)
        self.discount_limit = discount_limit
    
    # 修改 discount 折扣計算，加入確認折扣金額是否低於限制
    def calc_deduction(self):
        # deduction 為折扣百分比，小數點無條件捨去
        limit = self.discount_limit
        if self.discount > 0 and self.discount < 1:
            if int(self.discount * self.Order.order_sum()) > limit:
                return limit
            else: 
                return int(self.discount * self.Order.order_sum())
        # deduction 為折扣 y 元
        elif self.discount > 1:
            if self.discount > limit:
                return limit
            else:
                return self.discount
        # 未定義情況將報 ValueError
        else:
            raise ValueError('Please check promotion discount setting')

# 繼承 Promotion 類別，適用於訂單滿 x 元折 y% or z 元，全站有折抵金額上限
class Promotion_site_amount_limit(Promotion):
    def __init__(self, promotion_id, Order, threshold, discount, site_limit,site_usage):
        super().__init__(promotion_id, Order, threshold, discount)
        self.site_limit = site_limit
        self.site_usage = site_usage
    
     # 修改資格確認方式（加入驗證已使用金額）
    def meet_promotion_requirement(self):
        if self.Order.order_sum() >= self.threshold and self.site_limit > self.site_usage:
            return True
        else: 
            return False
    
    # 修改 discount 折扣計算，若折扣金額 > 可用餘額，回傳可用餘額
    def calc_deduction(self):
        # deduction 為折扣百分比，小數點無條件捨去
        if self.discount > 0 and self.discount < 1:
            if int(self.discount * self.Order.order_sum()) < self.site_limit - self.site_usage:
                return int(self.discount * self.Order.order_sum())
            else: 
                return self.site_limit - self.site_usage
        # deduction 為折扣 y 元
        elif self.discount > 1:
            if self.discount < self.site_limit - self.site_usage:
                return self.discount
            else: 
                return self.site_limit - self.site_usage
        # 未定義情況將報 ValueError
        else:
            raise ValueError('Please check promotion discount setting')