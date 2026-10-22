#!/usr/bin/env bash
# ============================================================================
# CHOICE 一键部署脚本（Ubuntu/Debian，腾讯云轻量香港）
# 用法：
#   sudo DOMAIN=choice.example.com REPO=https://.../choice.git EMAIL=you@xx.com bash deploy-choice.sh
# 前置：已绑密钥、防火墙开了 22/80/443（见部署文档第一步）。
# ============================================================================
set -e

DEPLOY_DIR=${DEPLOY_DIR:-/opt/choice-pm}
DOMAIN=${DOMAIN:-choice-goldsum-crm.duckdns.org}   # Choice 的 Duck DNS 子域名（同机 124.156.134.135）
PORT=${PORT:-5060}                                     # 与 AGI 错开
REPO=${REPO:-https://github.com/tomalso911-ship-it/vnchoicedouble}   # 你的 git 仓库
EMAIL=${EMAIL:-admin@example.com}                      # ← 改成你自己的邮箱（证书到期提醒）
APP_USER=${APP_USER:-root}

echo "==> 1) 安装系统依赖"
apt update
apt install -y python3 python3-venv python3-pip nginx git certbot python3-certbot-nginx

echo "==> 2) 拉取代码"
if [ -d "$DEPLOY_DIR/.git" ]; then
  git -C "$DEPLOY_DIR" pull --ff-only
else
  if [ -z "$REPO" ]; then
    echo "REPO 为空：请先把代码 scp 到 $DEPLOY_DIR，或设置 REPO 变量后重跑。"
    exit 1
  fi
  git clone "$REPO" "$DEPLOY_DIR"
fi

echo "==> 3) Python 虚拟环境 + 依赖"
python3 -m venv "$DEPLOY_DIR/.venv"
"$DEPLOY_DIR/.venv/bin/pip" install --upgrade pip
"$DEPLOY_DIR/.venv/bin/pip" install -r "$DEPLOY_DIR/requirements.txt"

echo "==> 4) systemd 常驻（端口 $PORT）"
cp "$(dirname "$0")/choice-pm.service" /etc/systemd/system/choice-pm.service
sed -i "s|^Environment=PORT=5060|Environment=PORT=$PORT|" /etc/systemd/system/choice-pm.service
systemctl daemon-reload
systemctl enable --now choice-pm
sleep 3
systemctl status choice-pm --no-pager | head -n 6

echo "==> 5) Nginx 反代 + 域名"
cp "$(dirname "$0")/nginx-choice.conf" /etc/nginx/sites-available/choice
sed -i "s/__DOMAIN__/$DOMAIN/g" /etc/nginx/sites-available/choice
ln -sf /etc/nginx/sites-available/choice /etc/nginx/sites-enabled/choice
nginx -t
systemctl reload nginx

echo "==> 6) HTTPS（certbot 自动签发 + 续期）"
certbot --nginx -d "$DOMAIN" --non-interactive --agree-tos -m "$EMAIL"

echo "==> 7) 验证"
curl -sS -o /dev/null -w "local http %{http_code}\n" http://127.0.0.1:$PORT/lite || true
curl -sS -o /dev/null -w "https %{http_code}\n" https://$DOMAIN/lite || true

echo "==> 完成。APK 的 server.url 指向 https://$DOMAIN 后用 node set-server.js 重打包。"
