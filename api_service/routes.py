from flask import jsonify, request
from api_service.db import get_connection

def register_routes(app):
    @app.route("/")
    def health_check():
        return {"status": "KEV API is running!"}

    @app.route("/vulnerabilities", methods=["GET"])
    def get_vulnerabilities():
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("SELECT * FROM kev_vulnerabilities ORDER BY date_added DESC LIMIT 100")
            data = cursor.fetchall()

            return jsonify(data)

        except Exception as e:
            return jsonify({"error": str(e)}), 500

        finally:
            cursor.close()
            conn.close()

    @app.route("/vulnerabilities/<cve_id>", methods=["GET"])
    def get_vulnerability_by_cve(cve_id):
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("SELECT * FROM kev_vulnerabilities WHERE cve_id = %s", (cve_id,))
            data = cursor.fetchone()

            if not data:
                return jsonify({"error": "CVE not found"}), 404

            return jsonify(data)

        except Exception as e:
            return jsonify({"error": str(e)}), 500

        finally:
            cursor.close()
            conn.close()
