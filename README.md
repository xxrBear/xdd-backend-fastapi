# 熊答答-AI答题应用平台

![Static Badge](https://img.shields.io/badge/build-_python_3.11-blue)
![Static Badge](https://img.shields.io/badge/fastapi_-green)

## 简介

基于编程导航 `鱼答答-AI答题应用平台` 后端项目，使用 FastAPI 框架重写。

- FastAPI 入门
- [yudada](https://github.com/liyupi/yudada) 前端接口无缝对接

## 功能完成度

✅ 基本CRUD业务接口

✅ 数据库模型自动创建

✅ 用户模块单元测试

✅ 统一异常工具函数

✅ 分页查询

✅ 统一的用户登录、权限检查

✅ 基于时间戳的递增id

## 快速部署

```
docker build -t xdd .
docker run -d -p 8102:8102 xdd
```

## 感谢

- [编程导航](https://www.codefather.cn/)
- [Pycharm](https://www.jetbrains.com/pycharm/)
