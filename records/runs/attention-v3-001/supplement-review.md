# 獲准補Wiki後的執行與覆蓋重檢

日期：2026-11-18，Asia/Taipei。批准依據為使用者原話「可以補wiki！再麻煩你了」。採前次建議A，先核對既有來源，不新增獨立來源；舊 attention-001 的狀態與修正歷史不動。

## 本次實際核對
| 既有來源 | 取得形式及讀取定位 | 用於補什麼 |
|---|---|---|
| Noba Attention | 網頁閱讀工具；The Cocktail Party、Dichotic Listening Studies、Divided Attention and Multitasking、Distracted Driving | 術語、熟練的自動化入門解釋、雙耳分聽與通話駕駛的教材轉述 |
| APA Multitasking: Switching costs | 網頁閱讀工具；What the research shows、What the research means、Sources & further reading | 2001年具名任務切換研究、任務類型與質性結果；1995年研究的可預期切換與準備結果 |
| Simons與Chabris作者網站PDF | 網頁閱讀工具；引言、§2方法、§3結果／Table 1 | 人名、1999、研究問題、傳球任務與條件、192／16／46% 的正確範圍 |
| Stroop原文HTML轉錄 | 網頁閱讀工具；引言pp.646–647、Experiments 1–2 pp.648–651 | 1935、研究背景、口語與色塊比較，不添加新的效應量 |
| PsyToolkit Stroop task | 網頁閱讀工具；Introduction及方法說明 | John Ridley Stroop全名、按鍵版本基準與短示範限制 |
| 吳彥文、游旭群2017 | 網頁閱讀工具；本次書目與中英摘要，配合既有全文讀取紀錄 | 自動化加工受條件調節的限定；不宣稱本次重新分析全文 |

來源網址及可用書目均收錄在 wiki/sources.md。本次不另下載原文封存，未生成文章內容雜湊；避免把工具可讀視為保存全文快照。來源筆記仍為前次版本，Wiki補充頁清楚區分本次再讀與沿用範圍。

## 補充後檔案清單
保留原9份：index、01-basics、02-selection、03-multitasking、04-stroop、05-applications、glossary、claims、uncertainties。
新增5份：06-research-origins（重要研究起源）；processing（自動化與主線）；07-related-experiments（雙耳與駕駛）；teaching-design（活動邊界）；sources（完整書目）。精確檔案與SHA-256見 wiki-inventory-after-supplement.json。

## 缺口結案方式
| 原缺口 | 狀態／本次做法 |
|---|---|
| G01 | 必要已補：原始研究引言、方法與數據定位進Wiki研究頁 |
| G02 | 必要已補：Stroop背景、年份、原始比較、完整姓名交叉核對 |
| G03 | 必要已補：採APA可支持的研究敘述，明示二手轉述；不冒稱已匯入原始切換論文 |
| G04 | 必要已補：入門正面定義、熟悉文字情境、注意條件與解釋的限制 |
| G05 | 選配已補：雙耳分聽與雞尾酒會，限Noba支持範圍，正文3作短註 |
| G06 | 選配已補：通話駕駛研究，限Noba支持範圍，正文14短註；不編造樣本或風險數字 |
| G07 | 配套已補：完整七份來源書目與中英術語；所有新故事先進Wiki才供大綱使用 |

「已補」不代表已重讀上述每篇教材引用的底層論文；目前大綱不需要超出這個支持層級，故沒有必要新增來源。若後續要求更細儀器、刺激、效應量或未記載的歷史背景，應重新列缺口。

## 逐頁覆蓋重檢
| 正文 | Wiki依據 | 結果／邊界 |
|---|---|---|
| 1 | 02-selection | 通過；用預測提問，不偽裝為盲測 |
| 2 | 01-basics、processing | 通過；三個問題是教學視角，不是固定神經流水線 |
| 3 | 01-basics、07-related-experiments、glossary | 通過；具名詞、例子與雙耳研究短註 |
| 4 | 06-research-origins、02-selection | 通過；起源／任務／數據／原理／限制齊備 |
| 5 | 02-selection、uncertainties | 通過；誤解澄清與熟悉／重測限制 |
| 6 | 03-multitasking、glossary | 通過；同時與切換對照、比較基準與例子 |
| 7 | 06-research-origins、03-multitasking | 通過；具名研究故事有二手來源定位 |
| 8 | teaching-design、03-multitasking | 通過；原創活動設計與研究證據分開；題數門檻待大綱批准 |
| 9 | 03-multitasking、teaching-design | 通過；結果、熟練條件與一次體驗限制 |
| 10 | 06-research-origins、processing | 通過；Stroop起源、自動化、生活情境與主線連結 |
| 11 | 04-stroop、teaching-design | 通過；按鍵作業及資料不足原則 |
| 12 | 04-stroop、teaching-design、uncertainties | 通過；集中解讀與限制，不提供假成績 |
| 13 | processing、05-applications | 通過；概念整合為教學整理 |
| 14 | 05-applications、07-related-experiments | 通過；生活應用、通話研究短註及回顧三問 |
| 封面／來源 | index、sources | 通過；不計入14頁正文 |

以上語意支持由本AI編輯核對，尚不是步驟4的兩道獨立審查。真實結構檢查見 supplement-outline-check.json：14份Wiki、115個本機連結、大綱14頁正文／16總頁、無相鄰同版型、至少4種版型、三頁草稿含6與8等檢查均通過。

## 當前停點
已完成具體大綱與正文6／7／8草稿，供人工關卡1。未寫全部逐頁稿、未執行兩道獨立審查、未生成兩頁HTML樣張或完整HTML，未宣稱教學品質已由非專業讀者實測。自動修正已用0輪；本次按授權補充與設計屬初次執行，不偽造修正紀錄。
