# 注意力 LLM Wiki

2026-11-21最新：使用者已確認簡報無問題，內容通過最終人工驗收。原交付包連結回報Codex服務錯誤，已驗證原ZIP完整，改以專案內的小型作業包及附加紀錄包提供下載。簡報與Wiki內容不變；遠端下載是否恢復仍需使用者端實際取得才能確認。

- [下載包說明](delivery/README.txt)
- [簡報HTML](attention-v3.html)
- [壓縮檔實際檢查](records/runs/attention-v3-001/delivery-service-check.json)

以下停點、待驗收描述及歷史交付連結為當時狀態。

2026-11-19最新退修：已補正文9、12的研究發現、原理、活動預期方向與實際結果解讀，並讓兩遊戲依方向顯示不同回饋。**仍待人工關卡3**。

- [最新單檔HTML](attention-v3.html)
- [這次修改與617項檢查](records/runs/attention-v3-001/feedback01-handoff.md)、[最新檢查表](records/runs/attention-v3-001/feedback01-checklist.md)
- [本次忠實度獨立審查](records/runs/attention-v3-001/fidelity-feedback01.json)、[教學品質逐頁審查](records/runs/attention-v3-001/teaching-feedback01.md)

2026-11-19目前交付：樣張已批准，**完整v3待人工關卡3驗收**。以下舊版停點為歷史，請以本段與v3狀態檔為準。

- [完整單檔離線HTML](attention-v3.html)：14頁正文＋封面＋來源，兩個互動遊戲；長頁可上下捲動。
- [驗收說明與實際結果](records/runs/attention-v3-001/final-handoff.md)：587項瀏覽器檢查通過，本機直接開檔因環境政策未驗證。
- [自我檢查表](records/runs/attention-v3-001/final-checklist.md)、[Wiki缺口處理](records/runs/attention-v3-001/gaps-status.md)
- [v3 Graph／Loop](workflow/v3-graph.md)、[實際反思素材](records/runs/attention-v3-001/observations.md)、[Git版本對照](records/runs/attention-v3-001/versions.md)

2026-11-19最新：v3大綱已批准，完整稿完成兩道獨立審查，目前**停在兩頁樣張的人工關卡2**。尚未製作完整v3 HTML。
- [兩頁離線HTML樣張](attention-v3-sample.html)：正文6多工對照＋正文8任務切換體驗。
- [本階段成果與限制](records/runs/attention-v3-001/sample-handoff.md)
- [忠實度重審](records/runs/attention-v3-001/fidelity-02.json)
- [逐頁教學品質審查表與獨立問答](records/runs/attention-v3-001/teaching-02.md)

2026-11-18 v3最新進度：使用者批准補Wiki後，已以既有來源補研究起源與術語；14頁正文的大綱與三頁草稿待人工關卡1。舊版以下驗收與修正額度均為歷史，不套用到v3。
- [v3具體大綱](content/v3/outline.md)
- [正文6、7、8的實際草稿](content/v3/three-page-drafts.md)
- [補Wiki與逐頁覆蓋重檢](records/runs/attention-v3-001/supplement-review.md)
- [研究起源](wiki/06-research-origins.md)及[完整來源表](wiki/sources.md)

最新：使用者退修後已完成第 3 輪，改為完整自行閱讀敘述與明確案例對照，排版採自然文流；獨立審查、446 項瀏覽器檢查及 12 項頁底捲動檢查通過。仍待最終人工驗收與本機離線補驗，剩餘修正輪次為 0（下文兩輪／一輪為前版歷史狀態，以本段及 state.json 為準）。
請使用 [新版簡報](slides/attention-self-study.html)；[本輪修改與檢查](records/runs/attention-001/revision-03.md)。較長頁面請在中央內容區上下捲動閱讀，底部導覽保留。

狀態：Wiki 與 12 頁大綱均已獲使用者確認。已完成獨立內容審查、離線 HTML 與四尺寸瀏覽器測試；等待本機直接開檔補驗及最終人工驗收。已用兩輪修正，剩餘一輪，勿重設 run。

驗收入口：
- [離線教學簡報](slides/index.html)：下載單一檔案即可使用，樣式與程式已內嵌。
- [驗收指引與實際結果](records/runs/attention-001/acceptance.md)
- [客觀反思素材](reflection/observations.md)
- [獨立審查報告](records/runs/attention-001/review-01.json)
- [最新瀏覽器報告](records/runs/attention-001/html-browser-final.json)

目前審閱入口：
- [12 頁教學大綱](content/outline.md)（含待確認的 Stroop 設定）
- [Graph 與 Loop 規則](workflow/README.md)
- [本次實際執行摘要](records/runs/attention-001/execution.md)
- [流程狀態](records/runs/attention-001/state.json)

主要入口：
- [Wiki 首頁](wiki/index.md)：五個主題頁、術語與限制。
- [來源登錄](sources/README.md)：七份正式來源筆記。
- [說法與引用對照](wiki/claims.md)：14 項知識說法及原文定位。
- [Wiki 實際檢查報告](records/checks/wiki-review.md)：本次結果與修正。
- [本次匯入紀錄](records/ingest/2026-11-16.md)：真實操作、取得限制及版本。

前期文件：
- `AGENTS.md`：已確認需求、階段界線及品質規則。
- `planning/structure.md`：資料夾與後續交付規劃。
- `planning/candidates.md`：當時的候選來源評估，保留為歷史；正式採用狀態以 sources/README.md 為準。
- `records/2026-11-16-source-search.md`：本次真實執行與檢查範圍。

下一步：等待使用者在本機直接開啟 HTML、確認離線操作及最終驗收；若回報錯誤，依共用上限及分類規則修正，不能重新初始化。

重跑結構檢查：在專案根目錄執行 `python tools/check_wiki.py`。此工具只檢查結構與引用存在性，科學內容支持度見人工編輯檢查紀錄。
