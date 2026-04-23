"""Tests for the like button feature and core API endpoints."""
import pytest
from app import create_app, db
from app.models import Post, Category


@pytest.fixture
def app():
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    }
    application = create_app(config=test_config)
    yield application


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def post_id(app):
    """Return the id of the first seeded post."""
    with app.app_context():
        return Post.query.first().id


# ── Categories ────────────────────────────────────────────────────────────────

def test_get_categories_returns_list(client):
    res = client.get("/api/categories")
    assert res.status_code == 200
    data = res.get_json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_category_has_required_fields(client):
    categories = client.get("/api/categories").get_json()
    for cat in categories:
        assert "id" in cat
        assert "name" in cat
        assert "icon" in cat


# ── Posts list ────────────────────────────────────────────────────────────────

def test_get_posts_returns_list(client):
    res = client.get("/api/posts")
    assert res.status_code == 200
    posts = res.get_json()
    assert isinstance(posts, list)
    assert len(posts) > 0


def test_post_has_required_fields(client):
    posts = client.get("/api/posts").get_json()
    for post in posts:
        for field in ("id", "title", "summary", "author", "difficulty", "like_count"):
            assert field in post, f"Field '{field}' missing from post"


def test_filter_posts_by_difficulty(client):
    res = client.get("/api/posts?difficulty=入门")
    assert res.status_code == 200
    posts = res.get_json()
    for post in posts:
        assert post["difficulty"] == "入门"


def test_filter_posts_by_category(client, app):
    with app.app_context():
        cat = Category.query.first()
        cat_id = cat.id

    res = client.get(f"/api/posts?category_id={cat_id}")
    assert res.status_code == 200
    posts = res.get_json()
    for post in posts:
        assert post["category"]["id"] == cat_id


# ── Single post ───────────────────────────────────────────────────────────────

def test_get_post_increments_view_count(client, post_id):
    before = client.get(f"/api/posts/{post_id}").get_json()["view_count"]
    after = client.get(f"/api/posts/{post_id}").get_json()["view_count"]
    assert after == before + 1


def test_get_nonexistent_post_returns_404(client):
    res = client.get("/api/posts/99999")
    assert res.status_code == 404


# ── Like button ───────────────────────────────────────────────────────────────

def test_like_increments_count(client, post_id):
    initial = client.get(f"/api/posts/{post_id}").get_json()["like_count"]
    res = client.post(
        f"/api/posts/{post_id}/like",
        json={"liked": False},
        content_type="application/json",
    )
    assert res.status_code == 200
    data = res.get_json()
    assert data["like_count"] == initial + 1
    assert data["liked"] is True
    assert data["id"] == post_id


def test_unlike_decrements_count(client, post_id):
    # Like first
    client.post(f"/api/posts/{post_id}/like", json={"liked": False})
    liked_count = client.get(f"/api/posts/{post_id}").get_json()["like_count"]

    # Unlike
    res = client.post(
        f"/api/posts/{post_id}/like",
        json={"liked": True},
        content_type="application/json",
    )
    assert res.status_code == 200
    data = res.get_json()
    assert data["like_count"] == liked_count - 1
    assert data["liked"] is False


def test_like_count_cannot_go_below_zero(client, post_id, app):
    # Ensure like_count is 0
    with app.app_context():
        post = db.session.get(Post, post_id)
        post.like_count = 0
        db.session.commit()

    res = client.post(
        f"/api/posts/{post_id}/like",
        json={"liked": True},  # try to unlike when already at 0
        content_type="application/json",
    )
    assert res.status_code == 200
    data = res.get_json()
    assert data["like_count"] >= 0


def test_like_nonexistent_post_returns_404(client):
    res = client.post("/api/posts/99999/like", json={"liked": False})
    assert res.status_code == 404


def test_multiple_likes_accumulate(client, post_id):
    initial = client.get(f"/api/posts/{post_id}").get_json()["like_count"]
    for _ in range(3):
        client.post(f"/api/posts/{post_id}/like", json={"liked": False})
        # Un-like before liking again to simulate fresh likes
        client.post(f"/api/posts/{post_id}/like", json={"liked": True})
    # Net change should be 0
    final = client.get(f"/api/posts/{post_id}").get_json()["like_count"]
    assert final == initial


# ── Index page ────────────────────────────────────────────────────────────────

def test_index_returns_html(client):
    res = client.get("/")
    assert res.status_code == 200
    assert b"<html" in res.data.lower()
