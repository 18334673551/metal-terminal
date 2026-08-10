# 投资研究终端 V3

完整 PWA 工程，兼容你现有 GitHub Pages `/metal-terminal/` 路径和 Android TWA 外壳。

## 功能
- 六大板块：有色、银行、券商、医药、制造业、科技
- 70 个关键指标
- 指标详情页 + 1M/3M/1Y/3Y/5Y/ALL 历史折线图
- 行业景气度评分
- 搜索、市场总览、深色移动端 UI
- PWA Manifest + Service Worker
- JSON 数据层
- GitHub Actions 数据格式校验

## 重要
当前 `data/history/*.json` 为 DEMO 演示序列，仅用于验证 UI 和图表，不是真实市场数据。

真实数据接入时，保持每个历史文件为：
```json
{"id":"copper_price","name":"铜价","unit":"USD/t","frequency":"日频","source":"真实数据源","is_demo":false,"updated":"2026-08-11","data":[["2026-08-10",9750],["2026-08-11",9820]]}
```
然后运行：
```bash
python scripts/update_data.py
```

## 部署
把 ZIP 解压后的内容上传/覆盖到现有 `metal-terminal` 仓库根目录。
GitHub Pages 继续使用 `main / (root)`。

只更新网页、图表、指标和 JSON 时，无需重新打 APK；现有 TWA APK 会继续打开：
`https://18334673551.github.io/metal-terminal/`

若要修改 Android 桌面上的应用名称，才需要重新构建 APK。
