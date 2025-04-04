from flask import Blueprint, current_app

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def root():
    return current_app.send_static_file("index.html")


@main_bp.route("/admin")
def admin_page():
    return current_app.send_static_file("index.html")


@main_bp.route("/log")
def log_page():
    return current_app.send_static_file("index.html")
