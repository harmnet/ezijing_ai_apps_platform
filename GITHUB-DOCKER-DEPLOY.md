# 使用GitHub Actions构建Docker镜像并部署

本文档说明如何利用GitHub Actions自动构建Docker镜像，并将其推送到GitHub Container Registry (ghcr.io)，然后在服务器上部署使用这些镜像。

## 配置GitHub仓库

### 1. 启用GitHub Container Registry

1. 访问GitHub设置页面，进入"Developer settings" > "Personal access tokens" > "Fine-grained tokens"
2. 生成一个新的访问令牌，赋予以下权限：
   - `read:packages` 和 `write:packages` - 用于访问和发布包
   - `repo` - 完整的仓库访问权限

### 2. 设置GitHub Actions

本仓库已经设置了自动化工作流（`.github/workflows/docker-build.yml`），当推送到主分支或手动触发工作流时，将自动构建并发布以下Docker镜像：

- 前端: `ghcr.io/[用户名]/ezijing-frontend:latest`
- 后端: `ghcr.io/[用户名]/ezijing-backend:latest`
- Node.js: `ghcr.io/[用户名]/ezijing-nodejs:latest`

## 构建过程

### 手动触发构建

1. 访问GitHub仓库页面
2. 点击"Actions"选项卡
3. 从左侧列表选择"Build and Push Docker Images"工作流
4. 点击"Run workflow"按钮，选择分支后点击绿色的"Run workflow"按钮

### 推送到主分支自动触发构建

每次向主分支（main或master）推送代码时，GitHub Actions会自动运行工作流构建镜像：

```bash
git add .
git commit -m "更新代码"
git push origin main
```

## 服务器部署

### 前提条件

- 服务器已安装Docker和Docker Compose
- 服务器可以访问互联网（访问ghcr.io）

### 部署步骤

1. 登录到服务器
2. 从GitHub克隆仓库或直接复制`docker-compose.ghcr.yml`和`deploy-ghcr.sh`文件
3. 给部署脚本添加执行权限：`chmod +x deploy-ghcr.sh`
4. 运行部署脚本：`./deploy-ghcr.sh`
5. 根据提示输入GitHub用户名和个人访问令牌（PAT）

### 验证部署

部署完成后，可访问以下地址验证服务是否正常运行：

- 前端: `http://服务器IP:8018`
- 后端: `http://服务器IP:9000`
- Node.js服务: `http://服务器IP:3000`

## 常见问题

### 无法拉取镜像

确保已经使用正确的凭据登录到GitHub Container Registry：

```bash
echo "你的GitHub PAT" | docker login ghcr.io -u 你的GitHub用户名 --password-stdin
```

### 镜像权限问题

默认情况下，GitHub Container Registry中的包是私有的。您需要在GitHub仓库的"Settings" > "Packages"中调整包可见性，或确保服务器已使用有权访问这些包的GitHub账户登录。

### 更新服务

当有新版本的镜像发布时，重新运行部署脚本即可更新服务：

```bash
./deploy-ghcr.sh
``` 