### 功能設計邏輯 ###

類別功能
- 使用者（User）：用戶資訊
- 產品（Product）：產品資訊
- 訂單（Order）：訂單資訊及計算「未折扣金額」的方法
- 折扣（Promotion）：折扣資訊，主要邏輯有 1|確認此訂單是否符合折扣資格、2|計算折扣金額
- 計算（Calculate）：計算「折扣後金額」，以字典輸出「未折扣金額」、「折扣金額」、「折扣後金額」，若需外加最終確認訂單邏輯（如折扣後金額不為零或負數，折抵金額不得大於特定異常大的數字（如折扣超過 10,000 NTD）），可以新建另一方法作為檢查再輸出

運用繼承設計數個 Promotion class（為方便維護，將 promotion 獨立成一檔案），對應指定的折扣情境，又因為 Promotion 拆為確認資格、計算折扣金額兩個主要邏輯，可以彈性增加新的使用情境和限制（需求）
