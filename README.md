# 个性化学习系统 · Personalized Learning System

一个轻量级的个性化学习内容管理框架，支持课程浏览、分类筛选和**一键点赞**功能。

## 功能特性

- 📚 学习内容（文章/课程）展示
- 🏷️ 按分类 / 难度筛选内容
- ❤️ **点赞按钮** — 为喜欢的内容点赞，再次点击取消
- 👁️ 浏览次数统计
- 📱 响应式界面，兼容移动端

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 启动服务（首次运行会自动建库并写入示例数据）
python run.py
```

浏览器访问 [http://localhost:5000](http://localhost:5000)

## API 端点

| 方法   | 路径                        | 说明             |
|--------|-----------------------------|------------------|
| GET    | `/api/posts`                | 获取文章列表     |
| GET    | `/api/posts?category_id=&difficulty=` | 筛选文章 |
| GET    | `/api/posts/<id>`           | 获取单篇文章详情 |
| POST   | `/api/posts/<id>/like`      | 点赞 / 取消点赞  |
| GET    | `/api/categories`           | 获取分类列表     |

### 点赞接口示例

```bash
# 点赞
curl -X POST http://localhost:5000/api/posts/1/like \
  -H "Content-Type: application/json" \
  -d '{"liked": false}'

# 取消点赞
curl -X POST http://localhost:5000/api/posts/1/like \
  -H "Content-Type: application/json" \
  -d '{"liked": true}'
```

## 运行测试

```bash
python -m pytest tests/ -v
```

## 技术栈

- **后端**：Python · Flask · SQLAlchemy · SQLite
- **前端**：原生 HTML / CSS / JavaScript（无框架依赖）
