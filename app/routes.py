from flask import Blueprint, jsonify, render_template, request, abort
from . import db
from .models import Post, Category

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/api/posts", methods=["GET"])
def get_posts():
    category_id = request.args.get("category_id", type=int)
    difficulty = request.args.get("difficulty")
    query = Post.query
    if category_id:
        query = query.filter_by(category_id=category_id)
    if difficulty:
        query = query.filter_by(difficulty=difficulty)
    posts = query.order_by(Post.like_count.desc(), Post.created_at.desc()).all()
    return jsonify([p.to_dict() for p in posts])


@main.route("/api/posts/<int:post_id>", methods=["GET"])
def get_post(post_id):
    post = db.get_or_404(Post, post_id)
    post.view_count += 1
    db.session.commit()
    return jsonify(post.to_dict())


@main.route("/api/posts/<int:post_id>/like", methods=["POST"])
def toggle_like(post_id):
    post = db.get_or_404(Post, post_id)
    action = request.get_json(silent=True) or {}
    liked = action.get("liked", False)

    if liked:
        post.like_count = max(0, post.like_count - 1)
        new_liked = False
    else:
        post.like_count += 1
        new_liked = True

    db.session.commit()
    return jsonify({"id": post.id, "like_count": post.like_count, "liked": new_liked})


@main.route("/api/categories", methods=["GET"])
def get_categories():
    categories = Category.query.all()
    return jsonify([c.to_dict() for c in categories])
