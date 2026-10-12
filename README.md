# Platform Monitor

遊戲平台監控儀表板 — 模擬遊戲/博弈平台的伺服器健康狀態監控系統，展示從 API 開發到容器化部署的完整流程。

## 功能

- 即時顯示多個服務的狀態、CPU 使用率、在線玩家數
- CPU 歷史趨勢圖表
- 背景排程自動持續收集監控資料
- 資料持久化，服務重啟不遺失歷史紀錄

## 技術棧

| 分類   | 技術                   |
| ------ | ---------------------- |
| 後端   | Flask (Python)         |
| 資料庫 | PostgreSQL             |
| 前端   | HTML + Chart.js        |
| 容器化 | Docker, docker-compose |
| 編排   | Kubernetes             |
| 排程   | cron / k8s CronJob     |

## 架構

使用者瀏覽器 → Flask (Pod) → PostgreSQL (Pod)，Flask 和 PostgreSQL 各自掛載 PVC 做資料持久化。

## 本機啟動（docker-compose）

docker-compose up --build

開啟 http://localhost:5001

## 部署到 Kubernetes

minikube start
eval $(minikube docker-env -u)
docker build -t platform-monitor-web:latest .
minikube image load platform-monitor-web:latest
minikube image load postgres:16
kubectl apply -f k8s/
minikube service web --url

## 專案結構

platform-monitor/app/ 底下是 main.py（Flask 主程式）、seed_data.py（獨立資料寫入腳本）、templates/index.html（前端儀表板）；k8s/ 放 Kubernetes manifests；根目錄有 Dockerfile、docker-compose.yml、requirements.txt。
