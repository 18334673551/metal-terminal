# V3.1 真实数据接入说明

## 已自动接入（FRED 官方 API）

当前第一批真实指标：

- 全球铜价（月均） -> `PCOPPUSDM`
- 全球铝价（月均） -> `PALUMUSDM`
- 全球锌价（月均） -> `PZINCUSDM`
- 全球镍价（月均） -> `PNICKUSDM`
- 美国 10Y 实际利率（日频） -> `DFII10`

这些指标更新后，详情页会显示 `LIVE` 和真实数据来源。

## 为什么没有把所有指标直接“硬接”上

为了避免把口径不一致的数据伪装成目标指标，V3.1 不会：

- 用“美联储广义美元指数”冒充 DXY；
- 用月度全球铜价冒充 LME 实时铜价；
- 用非官方网页抓取冒充 LME/SHFE 库存；
- 编造铜 TC/RC；
- 把商业数据库数据绕过许可抓取。

因此当前采用 `LIVE + DEMO/手工导入` 混合架构。

## GitHub 上启用 FRED 自动更新

1. 申请 FRED API key。
2. 打开 `metal-terminal` 仓库：
   `Settings -> Secrets and variables -> Actions -> New repository secret`
3. Name 填：
   `FRED_API_KEY`
4. Secret 填你的 API key。
5. 上传 V3.1 文件后，进入：
   `Actions -> Update real investment data -> Run workflow`
6. 成功后检查：
   `data/history/copper_price.json`
   其中应出现：
   `"is_demo": false`

工作流每天北京时间约 08:30 自动运行一次。

## TC/RC、LME/SHFE 库存

这类数据下一阶段建议采用：
- 官方交易所可下载数据；
- 你公司/个人已购买授权的数据接口；
- 手工下载 CSV 后由 `scripts/import_manual_csv.py` 导入。

示例：

```bash
python scripts/import_manual_csv.py ^
  --indicator copper_tc ^
  --file tc.csv ^
  --name "铜精矿TC" ^
  --unit "USD/dmt" ^
  --frequency "周频" ^
  --source "你的授权数据源"
```

然后运行：

```bash
python scripts/update_real_data.py
```

## 注意

真实数据接入后，历史趋势图、最新值和涨跌幅都无需改前端代码，会自动读取 JSON。
