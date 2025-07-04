import requests
import json
from datetime import datetime
from kev_fetcher.db import get_connection

KEV_FEED_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"

def fetch_and_store_kev():
    print("Fetching KEV catalog...")
    response = requests.get(KEV_FEED_URL)
    
    if response.status_code != 200:
        print(f"Failed to fetch data: {response.status_code}")
        return

    data = response.json()
    vulnerabilities = data.get("vulnerabilities", [])
    
    print(f"Found {len(vulnerabilities)} vulnerabilities.")
    conn = get_connection()
    cursor = conn.cursor()

    for vuln in vulnerabilities:
        try:
            cursor.execute("""
                INSERT IGNORE INTO kev_vulnerabilities (
                    cve_id,
                    vendor_project,
                    product,
                    vuln_name,
                    date_added,
                    due_date,
                    ransomware_use,
                    required_action,
                    notes,
                    related_cwe
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                vuln.get("cveID"),
                vuln.get("vendorProject"),
                vuln.get("product"),
                vuln.get("vulnerabilityName"),
                vuln.get("dateAdded"),
                vuln.get("dueDate"),
                vuln.get("knownRansomwareCampaignUse"),
                vuln.get("requiredAction"),
                vuln.get("notes"),
                ",".join(vuln.get("cwes", []))
            ))
        except Exception as e:
            print(f"Error inserting {vuln.get('cveID')}: {e}")
    
    conn.commit()
    cursor.close()
    conn.close()
    print("KEV data inserted into the database.")

if __name__ == "__main__":
    fetch_and_store_kev()
