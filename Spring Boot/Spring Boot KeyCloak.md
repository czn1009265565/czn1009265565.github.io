# Spring Boot KeyCloak

## 背景

Keycloak‌是一个开源的‌身份和访问管理(IAM)解决方案‌，主要用于现代应用程序和服务的身份验证和授权。
它提供了各种身份管理功能，帮助开发者和系统管理员轻松集成和管理用户认证、单点登录（SSO）和访问控制等功能‌

## 核心概念

### Realm

- 一个 Realm 表示一个完全隔离的身份和访问控制域
- 在 Keycloak 中，你可以创建多个独立的领域，每个领域都有自己的用户、客户端、角色和策略
- 用户在一个领域内进行注册、认证和授权

### Client

- 一个 Client 代表与 Keycloak 进行交互的应用程序或服务
- 客户端使用不同的协议（如 OpenID Connect、SAML、OAuth）与 Keycloak 进行集成
- Keycloak 的每个客户端都有自己的配置和安全设置，以及定义的受保护资源

### Role

- 角色表示一组权限或功能
- 在 Keycloak 中，你可以为每个客户端定义角色，并将角色分配给用户
- 角色用于授权和访问控制，通过为用户授予特定角色来确定他们能够执行哪些操作或访问哪些资源

### User

- 用户是使用应用程序或服务的最终用户

### Group

- 组用于组织和管理用户
- 在 Keycloak 中，你可以创建组，并将用户分配到组中
- 组可以与角色相关联，以实现对组内用户的授权管理

## 安装部署

下载地址: https://www.keycloak.org/downloads

### 解压启动

```shell
# 解压
unzip keycloak-21.0.0.zip 
cd keycloak-21.0.0
# Linux启动
bin/kc.sh start-dev
# Windows启动
bin/kc.bat start-dev
```
运行启动命令后，打印`Keycloak 21.0.0 on JVM started`则表示启动服务成功。

### 创建管理员

1. 访问 `http://localhost:8080`
2. 输入用户名和密码以创建管理员进行登录


### 创建 Realm

1. 导航到左上角，找到 "Create realm" 按钮
2. 这里添加一个名为 "myrealm" 的新 "Realm"。

### 创建用户

1. 点击左侧Users菜单栏
2. 点击Create new user
3. 点击Credentials设置密码
4. 验证登录，访问 `http://localhost:8080/realms/myrealm/account/#/`


### 保护第一个应用程序

1. 访问控制台 `http://localhost:8080/admin`
2. 点击Clients
3. 点击Create client
4. 表单填写  
   - Client type: OpenID Connect
   - Client ID: myclient
   - Standard flow: enabled
   - Valid redirect URIs: 应用重定向URL，例如 `http://localhost:8888/*`
   - Web origins: `http://localhost:8888/`

