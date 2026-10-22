#!/usr/bin/env bash
# ============================================================================
# CHOICE 异地备份：把本地滚动备份里【最新一份】每日上传到腾讯云 COS。
# 前置：安装 coscli（https://cloud.tencent.com/document/product/436/63144）
#      并配置 ~/.cos.yaml（coscli config add 生成）。
# 用法：crontab -e 加一行  →  30 3 * * *  /opt/choice-pm/deploy/backup-cos.sh
# ============================================================================
set -e

DEPLOY_DIR=${DEPLOY_DIR:-/opt/choice-pm}
BACKUP_DIR="$DEPLOY_DIR/backups"          # app.py 每 30 分钟滚动保留 80 份的地方
COS_BUCKET=${COS_BUCKET:-choice-pm-backup-1250000000}   # ← 改成你的存储桶(含APPID)
COS_PREFIX=${COS_PREFIX:-agipm-db}

echo "==> 找最新一份本地备份"
LATEST=$(ls -1t "$BACKUP_DIR"/*.sqlite3.bak 2>/dev/null | head -n 1 || true)
if [ -z "$LATEST" ]; then
  echo "未找到备份文件，跳过。"
  exit 0
fi

TODAY=$(date +%Y%m%d)
DEST="$COS_PREFIX/$TODAY-$(basename "$LATEST")"

echo "==> 上传 $LATEST -> cos://$COS_BUCKET/$DEST"
coscli cp "$LATEST" "cos://$COS_BUCKET/$DEST"

echo "==> 完成：$DEST"
