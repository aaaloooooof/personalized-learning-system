import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()


def create_app(config=None):
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///learning.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "change-me-in-production")

    if config:
        app.config.update(config)

    CORS(app)
    db.init_app(app)

    from .routes import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()
        _seed_data()

    return app


def _seed_data():
    from .models import Post, Category
    if Post.query.count() == 0:
        categories = [
            Category(name="数学", icon="📐"),
            Category(name="编程", icon="💻"),
            Category(name="语文", icon="📖"),
            Category(name="英语", icon="🌍"),
            Category(name="科学", icon="🔬"),
        ]
        db.session.add_all(categories)
        db.session.flush()

        posts = [
            Post(
                title="Python 入门：从零开始学编程",
                summary="本课程面向零基础学习者，涵盖 Python 基础语法、数据类型、控制流和函数等核心概念，帮助你快速上手编程。",
                content="Python 是一种简洁易学的编程语言……",
                category_id=categories[1].id,
                author="张三",
                difficulty="入门",
                duration=60,
            ),
            Post(
                title="高中数学：导数与微积分基础",
                summary="深入讲解导数的概念、求导法则及其在实际问题中的应用，帮助学生建立扎实的微积分基础。",
                content="导数是描述函数变化率的重要工具……",
                category_id=categories[0].id,
                author="李四",
                difficulty="中级",
                duration=90,
            ),
            Post(
                title="现代汉语写作技巧",
                summary="系统讲解议论文、说明文、记叙文的写作方法，通过大量范文分析提升写作水平。",
                content="写作是表达思想的重要方式……",
                category_id=categories[2].id,
                author="王五",
                difficulty="入门",
                duration=45,
            ),
            Post(
                title="英语口语：日常会话提升",
                summary="通过情景对话练习，帮助学习者掌握日常英语交流技巧，提升听说能力。",
                content="流利的英语口语需要大量练习……",
                category_id=categories[3].id,
                author="赵六",
                difficulty="中级",
                duration=50,
            ),
            Post(
                title="初中物理：力学与运动",
                summary="系统介绍牛顿运动定律、摩擦力、重力等基础力学知识，配合实验演示加深理解。",
                content="力学是物理学的重要分支……",
                category_id=categories[4].id,
                author="孙七",
                difficulty="入门",
                duration=75,
            ),
            Post(
                title="数据结构与算法：排序算法详解",
                summary="深入分析冒泡排序、快速排序、归并排序等常见排序算法的原理、实现与复杂度分析。",
                content="排序算法是计算机科学的基础……",
                category_id=categories[1].id,
                author="周八",
                difficulty="进阶",
                duration=120,
            ),
        ]
        db.session.add_all(posts)
        db.session.commit()
