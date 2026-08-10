# 有色金属投资终端 V2 — 手机优先 PWA

## V2 新增
- 手机优先界面
- 底部 App 导航：首页 / 宏观 / 铜 / 铝 / 黄金
- PWA Web App Manifest
- Service Worker 离线缓存
- “安装到手机桌面”入口（支持 beforeinstallprompt 的浏览器）
- iOS Web App 元信息与 Apple Touch Icon
- 网络优先更新 `data/latest.json`，失败自动使用离线/内嵌数据
- 铜 / 铝 / 黄金独立驱动页
- GitHub Actions 保留日更数据能力

## 本地运行
PWA 的 Service Worker 不能可靠地从 `file://` 直接运行。

Windows：
双击 `start_windows.bat`

或：
```bash
python -m http.server 8000
```
打开：
http://localhost:8000

## 免费部署
### GitHub Pages
1. 新建一个 GitHub 仓库。
2. 把本项目全部文件上传到仓库根目录。
3. Settings → Pages。
4. Source 选择 `Deploy from a branch`。
5. Branch 选择 `main` + `/root`。
6. 保存并等待生成 HTTPS 地址。

PWA/Service Worker 在 HTTPS 或 localhost 环境下工作最佳。

## 手机安装
### Android / Chrome
打开部署后的 HTTPS 地址。如果浏览器判断可安装，首页会出现“安装到手机桌面”按钮，也可用浏览器菜单安装应用。

### iPhone / Safari
打开部署后的地址 → 分享 → 添加到主屏幕。iOS 的安装入口由 Safari 提供，不一定触发网页内的安装按钮。

## 目录
- index.html：V2 App UI
- manifest.webmanifest：PWA 清单
- sw.js：离线缓存
- icons/：App 图标
- data/latest.json：数据
- scripts/update_data.py：自动更新脚本
- .github/workflows/update.yml：每日 GitHub Actions

## 下一阶段 V3
建议新增：
- 铜 / 铝 / 金现货与期货价格
- LME / SHFE 库存
- 铜精矿 TC/RC
- 供需平衡表
- 历史分位
- 金属景气评分引擎
- 紫金矿业 / 洛阳钼业 / 江西铜业 / 中国铝业等公司页
