# 实验室管理系统前端

本项目使用 [Create React App](https://github.com/facebook/create-react-app) 和 TypeScript 构建。

## 环境准备

- Node.js (推荐 LTS 版本，例如 v18.x 或 v20.x)
- npm (通常随 Node.js 一起安装) 或 yarn

## 本地开发

### 1. 克隆仓库 (如果尚未克隆)
```bash
git clone git@github.com:Diss-Lab/Lab-framework.git
cd Lab-framework/frontend
```

### 2. 安装依赖
进入 `frontend` 目录后，运行以下命令安装项目依赖：

如果你使用 npm:
```bash
npm install
```

或者，如果你使用 yarn:
```bash
yarn install
```
这将会在 `frontend` 目录下创建 `node_modules` 文件夹并下载所有必要的包。

### 3. 启动开发服务器
```bash
npm start
```
或者 (使用 yarn):
```bash
yarn start
```
这会在开发模式下运行应用。
在浏览器中打开 [http://localhost:3000](http://localhost:3000) 查看。

每次修改代码后，页面会自动重新加载。你也可以在控制台中看到任何 lint 错误。

### 4. 构建生产版本
```bash
npm run build
```
或者 (使用 yarn):
```bash
yarn build
```
这会将应用构建为静态文件，输出到 `build` 文件夹。

## 注意事项
- `node_modules` 文件夹不应提交到 Git 仓库，它由 `npm install` 或 `yarn install` 自动生成。
- `package-lock.json` (或 `yarn.lock`) 文件 **应该** 提交到 Git 仓库，以确保所有开发者和构建环境使用相同版本的依赖。
