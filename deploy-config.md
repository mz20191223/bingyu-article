# 冰鱼发布系统 - 部署配置文档

> 更新日期：2026-07-01（最终状态）

---

## 一、项目信息

| 项目 | 详情 |
|------|------|
| 项目名称 | 冰鱼自动发布系统 |
| 技术栈 | 前端 Vue3 + Element Plus / 后端 Flask + MySQL + Playwright |
| 本地路径 | `D:\python project\auto_publish.py\new article` |
| GitHub | `mz20191223/bingyu-article`（Public） |
| 默认账号 | `admin` / `123456` |

---

## 二、前端部署（Cloudflare Pages）

| 项目 | 详情 |
|------|------|
| 平台 | Cloudflare Pages |
| 访问地址 | `https://bingyu-article.pages.dev` |
| 构建框架 | Vue.js |
| 构建命令 | `cd frontend && npm install && npm run build` |
| 输出目录 | `frontend/dist` |
| 环境变量 | `VITE_API_BASE_URL` |

### 当前 API 地址

```
https://surprised-allocation-determines-dogs.trycloudflare.com
```

> ⚠️ 这是 Cloudflare Tunnel 临时地址，服务器重启后会变化。重启后需更新此变量。

### 更新部署方式

1. 推代码到 GitHub → Cloudflare 自动构建
2. 或修改环境变量后点击 Retry deployment

### 本地开发

```bash
cd "D:\python project\auto_publish.py\new article\frontend"
npm run dev           # 开发模式，走 Vite 代理 → localhost:5005
npm run build         # 生产构建
```

### 环境变量说明

- `VITE_API_BASE_URL`：设置后端 API 地址
- 开发模式：不设置（走 Vite 代理）
- 生产模式：设为 HTTPS 地址（Cloudflare Tunnel 或域名）

---

## 三、后端部署（腾讯云轻量服务器）

### 服务器信息

| 项目 | 详情 |
|------|------|
| 云平台 | 腾讯云轻量应用服务器 |
| 配置 | 2核4G / 5M 带宽 / 60GB SSD / 500GB 流量 |
| 系统 | Ubuntu 22.04 LTS |
| 地域 | 广州 |
| 公网 IP | `129.204.189.218` |
| 内网 IP | `10.1.0.5` |
| 当前套餐 | 免费试用 1 个月（到期前建议购买 528元/3年） |

### 服务架构

```
用户浏览器
    ↓ HTTPS
Cloudflare Pages (bingyu-article.pages.dev)
    ↓ HTTPS
Cloudflare Tunnel (xxx.trycloudflare.com)
    ↓ HTTP localhost:5000
Flask 后端 (127.0.0.1:5000)
    ↓
MySQL (127.0.0.1:3306)
```

### 后端路径

```
/opt/bingyu-article/backend/
```

### 启动命令（服务器重启后）

```bash
# 启动 Cloudflare 隧道
cloudflared tunnel --url http://localhost:5000 &

# 启动 Flask 后端
cd /opt/bingyu-article/backend
sudo venv/bin/python run.py &

# 拿到新 Tunnel URL 后更新 Cloudflare Pages 环境变量
```

### Python 虚拟环境

```
/opt/bingyu-article/backend/venv/
```

### 数据库

| 项目 | 详情 |
|------|------|
| 数据库 | MySQL 8.0 |
| 数据库名 | `soft_article_db` |
| 用户名 | `root` |
| 密码 | `123456` |
| 认证方式 | mysql_native_password |
| 远程访问 | ✅ 已开启 |

### Navicat 远程连接

| 参数 | 值 |
|------|-----|
| 主机 | `129.204.189.218` |
| 端口 | `3306` |
| 用户名 | `root` |
| 密码 | `123456` |

### MySQL 远程访问命令

```bash
mysql -u root -p'123456' -e "CREATE USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY '123456';"
mysql -u root -p'123456' -e "GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION; FLUSH PRIVILEGES;"
```

### 已安装服务

- Python 3.10 + venv
- MySQL 8.0
- Nginx（已安装，未配置）
- Certbot（已安装，未配置）
- Playwright + Chromium
- cloudflared（Cloudflare Tunnel）
- lrzsz（文件传输）

### 腾讯云防火墙规则

| 端口 | 协议 | 来源 | 用途 |
|------|------|------|------|
| 5000 | TCP | 全部IPv4 | Flask 后端 |
| 3306 | TCP | 全部IPv4 | MySQL 远程连接 |
| 8080 | TCP | 全部IPv4 | 临时文件上传 |
| 5005 | TCP | 全部IPv4 | 预留备用 |

---

## 四、Cloudflare Tunnel

| 项目 | 详情 |
|------|------|
| 当前 URL | `https://surprised-allocation-determines-dogs.trycloudflare.com` |
| 作用 | 为 HTTP 后端提供免费 HTTPS 隧道 |
| 特点 | 免费、自动 SSL、无需域名 |
| 缺点 | 服务器重启后 URL 会变 |
| 工具路径 | `/usr/local/bin/cloudflared` |

---

## 五、数据同步

| 项目 | 详情 |
|------|------|
| 方式 | Navicat 数据传输 |
| 源 | MZPC（本地） → 目标：个人服务器（远程） |
| 状态 | ✅ 已完成 |

---

## 六、Cloudflare 账号

| 项目 | 详情 |
|------|------|
| 登录方式 | GitHub（mz20191223） |
| 管理后台 | https://dash.cloudflare.com |
| 网站 URL | https://bingyu-article.pages.dev |

---

## 七、GitHub 信息

| 项目 | 详情 |
|------|------|
| 用户名 | mz20191223 |
| 仓库 | mz20191223/bingyu-article |
| 可见性 | Public |
| Token | ⚠️ 已暴露，建议重新生成 |

---

## 八、提醒事项

- [x] 前端部署到 Cloudflare Pages
- [x] 服务器部署后端
- [x] 数据库初始化
- [x] 数据同步（Navicat）
- [x] Cloudflare Tunnel HTTPS
- [x] 系统可正常登录使用
- [ ] 购买域名 + Nginx + SSL（可选，替代 Tunnel）
- [ ] 配 AI API Key（`/opt/bingyu-article/backend/.env`）
- [ ] 删除已暴露的 GitHub Token，重新生成
- [ ] 免费试用到期前换购 528元/3年 套餐
- [ ] 服务器重启后更新 Cloudflare Pages 的 `VITE_API_BASE_URL`
