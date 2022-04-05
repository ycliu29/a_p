### 類別設計邏輯 ###

設計邏輯
遵從 SOLID 原則，高內聚、低耦合，偏好 composition 多於 inheritance

- User：用戶資訊
- Product：產品資訊
- Order：訂單資訊及計算訂單總金額（不考慮 promotion）的方法
- Promotion：折扣資訊，包括折扣門檻、折扣折數、金額或贈品，以數個 subclass 加入折扣限制（全站使用次數、每單優惠上限、每月折扣上限）
- Promo_Requirement_Checker：檢查訂單是否符合折扣門檻，抽象類別為基礎，以 subclass 處理各邏輯（訂單達 x 元、訂單有 y 物品 N 個、訂單達 x 元且折扣尚未用盡，小於折扣使用次數限制）
- Promo_Deduction_Calculator：計算訂單折扣金額，抽象類別為基礎，以 subclass 處理各邏輯（折 z%、送特定產品、折 x% 但每單上限 y 元、折 k 元但此折扣全站上限為 l 元）
- Calculator：輸出計算後結果，需搭配情境對應的 Promo_Requirement_Checker 和 Promo_Deduction_Calculator。有數個 subclass 以處理無 promo、折抵金額和免費物品的情境，

#### 改版紀錄 ####
- 增加 type hints
- 以 coverage.py 確認功能都已測試
- 大幅度移除方法中不必要的 if else
- 從 Order 類別中移除 Promotion, User(fields)
- 新增 abstract classes
