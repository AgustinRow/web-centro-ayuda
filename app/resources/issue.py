from flask import redirect, render_template, request, url_for
from app.db import connection
from app.models.issue import Issue
from sqlalchemy import or_

# Public resources


def index():

    issues = Issue.query.all()
    print(issues)
    return render_template("issue/index.html", issues=issues)


def new():
    return render_template("issue/new.html")


def create():
    conn = connection()
    Issue.create(conn, request.form)

    return redirect(url_for("issue_index"))
