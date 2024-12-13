# 熊答答-AI答题应用平台

![Static Badge](https://img.shields.io/badge/build-_python_3.11-blue)
![Static Badge](https://img.shields.io/badge/FastAPI_-green)
![Static Badge](https://img.shields.io/badge/SQLModel-8A2BE2)
![Static Badge](https://img.shields.io/badge/Pydantic-red)
![Static Badge](https://img.shields.io/badge/ChatGLM-%E6%99%BA%E8%B0%B1AI-%230746ff)

## 简介

基于编程导航 `鱼答答-AI答题应用平台` 后端项目，使用 FastAPI 框架重写。

- FastAPI 项目入门
- ChatGLM 大模型入门
- 与 [yudada](https://github.com/liyupi/yudada) 前端项目无缝对接

## 功能完成度

✅ 基本CRUD业务功能

✅ 统一异常处理中间件

✅ 统一用户登录、权限检查中间件

✅ 平台智能化

✅ Docker 自动化部署

> 本项目旨在练习 FastAPI 框架以及上手 ChatGLM 大模型的使用。许多功能仅为看起来“正常工作”，不能满足所有的边界场景。

## 快速部署

```
docker build -t xdd .
docker run -d -p 8102:8102 xdd
```

## 感谢

- [编程导航](https://www.codefather.cn/)
