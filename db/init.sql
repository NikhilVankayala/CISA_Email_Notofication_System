CREATE TABLE IF NOT EXISTS kev_vulnerabilities (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cve_id VARCHAR(50) NOT NULL UNIQUE,
    vendor_project VARCHAR(255),
    product VARCHAR(255),
    vuln_name TEXT,
    date_added DATE,
    due_date DATE,
    ransomware_use VARCHAR(50),
    required_action TEXT,
    notes TEXT,
    related_cwe TEXT
);

CREATE TABLE subscribers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE
);