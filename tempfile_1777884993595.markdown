# AI Chat System

基于 FastAPI 构建的智能聊天系统，集成 Moonshot AI（Kimi）提供智能对话功能，支持用户注册登录、JWT 认证和聊天记录管理。

## 📋 目录

- [项目简介](#项目简介)
- [技术栈](#技术栈)
- [项目结构](#项目结构)
- [功能特性](#功能特性)
- [安装与配置](#安装与配置)
- [API 接口文档](#api-接口文档)
- [数据库设计](#数据库设计)
- [认证机制](#认证机制)
- [使用示例](#使用示例)
- [开发说明](#开发说明)

---

## 🎯 项目简介

AI Chat System 是一个现代化的智能聊天应用后端系统，采用 FastAPI 框架构建，具备以下核心能力：

- ✅ 用户注册与登录系统
- ✅ JWT Token 身份认证
- ✅ 集成 Moonshot AI（Kimi）智能对话
- ✅ 聊天记录持久化存储
- ✅ RESTful API 设计
- ✅ 密码 bcrypt 加密保护

---

## 🛠️ 技术栈

### 后端框架
- **FastAPI** - 高性能异步 Web 框架
- **SQLAlchemy** - Python ORM 数据库工具
- **Pydantic** - 数据验证和序列化

### 安全认证
- **python-jose** - JWT Token 编解码
- **passlib** - 密码哈希加密（bcrypt）

### AI 集成
- **openai** - Moonshot AI API 客户端

### 数据库
- **MySQL** - 关系型数据库（通过 PyMySQL 连接）

---

## 📁 项目结构

ai-chat-system/
├── app.py                # 应用入口，路由注册
├── auth.py               # 认证模块（JWT、密码加密）
├── models.py             # 数据库模型（ORM）
├── schemas.py            # Pydantic 数据验证模型
├── database.py           # 数据库连接配置
├── crud.py               # 数据库操作（待实现）
├── requirements.txt      # Python 依赖包
├── routers/              # 路由模块
│   ├── user.py           # 用户相关接口（注册、登录）
│   └── chat.py           # 聊天相关接口
└── test.db               # SQLite 数据库文件（备用）

### 核心文件说明

| 文件 | 作用 | 关键功能 |
|------|------|---------|
| `app.py` | 应用主入口 | 创建 FastAPI 实例，注册路由 |
| `auth.py` | 认证模块 | JWT 生成/验证、密码加密/验证 |
| `models.py` | 数据库模型 | 定义 UserDB、ChatDB 表结构 |
| `schemas.py` | 数据验证 | 定义 API 请求/响应数据结构 |
| `database.py` | 数据库配置 | 创建数据库引擎和会话工厂 |
| `routers/user.py` | 用户路由 | 注册、登录接口实现 |
| `routers/chat.py` | 聊天路由 | AI 对话接口实现 |

---

## ✨ 功能特性

### 1. 用户管理
- 用户注册（密码自动 bcrypt 加密）
- 用户登录（密码验证 + JWT Token 发放）
- 密码长度限制（最多 72 字符，bcrypt 限制）

### 2. 身份认证
- JWT Bearer Token 认证
- Token 有效期：60 分钟
- 自动验证 Token 有效性
- 受保护的路由自动拦截未授权请求

### 3. 智能聊天
- 集成 Moonshot AI（Kimi）大语言模型
- 实时 AI 对话生成
- 聊天记录自动保存到数据库
- 需要认证才能访问聊天接口

### 4. 数据安全
- 密码 bcrypt 加密存储
- JWT Token 签名验证
- SQL 注入防护（ORM）
- 输入数据验证（Pydantic）

---

## 🚀 安装与配置

### 前置要求

- Python 3.8+
- MySQL 数据库（或使用 SQLite）
- Moonshot AI API Key

### 安装步骤

#### 1. 克隆项目
---

#### 2. 用户注册

**接口**: `POST /user/register`

**描述**: 注册新用户账号

**请求体**:
json { "username": "john", "password": "secret123" }**成功响应** (200):
**成功响应** (200):
json { "msg": "注册成功" }
**错误响应** (400):
json { "detail": "密码太长（最多72字符）" }
---

#### 4. 发送聊天消息

**接口**: `POST /chat/`

**描述**: 发送问题给 AI 并获取回答（需要认证）

**认证**: 需要 Bearer Token
---

### API 文档自动生成

FastAPI 自动生成交互式 API 文档：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🗄️ 数据库设计

### 数据库表结构

#### 1. users 表（用户表）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | 用户 ID |
| username | VARCHAR(50) | NOT NULL | 用户名 |
| password | VARCHAR(100) | NOT NULL | 密码（bcrypt 加密） |

 客户端 │ │ 服务器 │ │ 数据库 │ └────┬─────┘ └────┬─────┘ └────┬─────┘ │ │ │ │ 1. 登录请求 │ │ │ (username/password)│ │ │ ──────────────────> │ │ │ │ 2. 验证用户 │ │ │ ──────────────────> │ │ │ <────────────────── │ │ │ 3. 生成 JWT Token │ │ 4. 返回 Token │ │ │ <────────────────── │ │ │ │ │ │ 5. 携带 Token 请求 │ │ │ Authorization: │ │ │ Bearer <token> │ │ │ ──────────────────> │ │ │ │ 6. 验证 Token │ │ │ (解码 + 检查过期) │ │ 7. 返回数据 │ │ │ <────────────────── │ │


