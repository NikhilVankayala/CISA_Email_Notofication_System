from datetime import datetime, timedelta
from email_service.db import get_connection
from email_service.email_utils import send_email

def get_subscribers():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM subscribers")
    emails = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return emails

def get_recent_vulnerabilities(hours=24):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    since = (datetime.utcnow() - timedelta(hours=hours)).strftime('%Y-%m-%d')
    cursor.execute("""
        SELECT * FROM kev_vulnerabilities 
        WHERE date_added >= %s
        ORDER BY date_added DESC
    """, (since,))

    vulns = cursor.fetchall()
    cursor.close()
    conn.close()
    return vulns

def format_email_html(vulns):
    if not vulns:
        return "<p>No new vulnerabilities added in the last 24 hours.</p>"

    html = "<h2>New Known Exploited Vulnerabilities</h2><ul>"
    for v in vulns:
        html += f"""
        <li>
            <strong>{v['cve_id']}</strong> - {v['vuln_name']}<br>
            <em>{v['vendor_project']} / {v['product']}</em><br>
            <p><strong>Action:</strong> {v['required_action']}</p>
            <hr>
        </li>
        """
    html += "</ul>"
    return html

def main():
    print("🔎 Fetching recent vulnerabilities...")
    vulns = get_recent_vulnerabilities()

    if not vulns:
        print("✅ No new KEVs to send.")
        return

    print(f"📬 Found {len(vulns)} new vulnerabilities. Fetching subscribers...")
    subscribers = get_subscribers()

    if not subscribers:
        print("⚠️ No subscribers found. Exiting.")
        return

    html = format_email_html(vulns)

    for email in subscribers:
        print(f"✉️ Sending email to {email}")
        send_email(email, "🚨 New KEV Vulnerabilities Alert", html)

if __name__ == "__main__":
    main()
