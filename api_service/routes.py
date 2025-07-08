from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from api_service.db import get_connection

def register_routes(app):
    @app.route("/")
    def home():
        user_name = session.get("user_name")
        return render_template("home.html", user=user_name)

    @app.route("/signup", methods=["GET", "POST"])
    def signup():
        if request.method == "POST":
            name = request.form["name"]
            wants_alerts = 'wants_alerts' in request.form

            email = request.form.get("email") if wants_alerts else None
            password = request.form["password"]

            if wants_alerts and not email:
                flash("Email is required if you want alerts.", "danger")
                return render_template("signup.html")

            hashed_pw = generate_password_hash(password)

            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO subscribers (name, email, password_hash, wants_alerts) VALUES (%s, %s, %s, %s)",
                    (name, email, hashed_pw, wants_alerts)
                )
                conn.commit()
                flash("Account created successfully. Please log in.", "success")
                return redirect(url_for("login"))
            except Exception as e:
                flash(f"Error: {e}", "danger")
            finally:
                cursor.close()
                conn.close()

        return render_template("signup.html")


    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]

            try:
                conn = get_connection()
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM subscribers WHERE email = %s", (email,))
                user = cursor.fetchone()

                if user and check_password_hash(user["password_hash"], password):
                    session["user_id"] = user["id"]
                    session["user_name"] = user["name"]
                    return redirect(url_for("vulnerabilities_page"))
                else:
                    flash("Invalid email or password.", "danger")
            finally:
                cursor.close()
                conn.close()

        return render_template("login.html")


    @app.route("/logout")
    def logout():
        session.clear()
        flash("You have been logged out.", "info")
        return redirect(url_for("login"))


    @app.route("/vulnerabilities")
    def vulnerabilities_page():
        if "user_id" not in session:
            return redirect(url_for("login"))

        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM kev_vulnerabilities ORDER BY date_added DESC LIMIT 100")
            data = cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

        return render_template("vulnerabilities.html", data=data, user=session.get("user_name"))
