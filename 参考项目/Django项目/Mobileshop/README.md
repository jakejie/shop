# Mobileshop

一个手机网页端商城 Demo (Vue + Django)

运行环境：
- Python 3.6.3
- Django 1.11.7

建议开 Virtualenv 跑

## 开始

### 1. 克隆到本地

```
git clone https://github.com/Agrimonia/Mobileshop.git
cd Mobileshop
```

### 2. 测试

> Dev 分支在本地测试用 SQLite3 即可，master 分支用 mysql 需要配置 mysql.cnf

```bash
# 前端部分
cd frontend
npm install
npm build
npm run dev
```

```bash
# 后端部分

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### 3. 开发进度

- [x] Hello World
- [x] 数据库换成 MySQL，用 Postman 测试接口可用
- [ ] 根据需求设计数据库
- [ ] 用户注册登录
- [ ] 商品管理
- [ ] 前端浏览、购买商品
- [ ] 生产环境部署
