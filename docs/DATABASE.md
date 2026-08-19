# DATABASE ARCHITECTURE — SK AI 4.0 (PROJECT JARVIS 4.0)

**Platform Version:** Jarvis Platform V5.0  
**Storage Engine:** SQLite 3 (WAL Mode Enabled)  
**ORM Framework:** SQLAlchemy 2.0  
**Database Location:** `%APPDATA%\SK Enterprises\SK AI 4.0\sk_ai_master.db`  

---

## 1. STORAGE ARCHITECTURE & UAC SAFETY

To guarantee 100% reliability across all Windows installations, the application utilizes a platform-safe directory structure under user-specific `%APPDATA%`.

```text
C:\Users\<User>\AppData\Roaming\SK Enterprises\SK AI 4.0\
├── sk_ai_master.db               # Primary SQLite relational database
├── logs\                         # Structured log files (application.log, error.log)
└── storage\                      # Encrypted client key manifests & data
```

---

## 2. RELATIONAL SCHEMA DEFINITIONS

### 2.1 `users` Table
Stores registered system operators and client accounts.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique user identifier |
| `name` | VARCHAR(100) | NOT NULL | User / Client full name |
| `email` | VARCHAR(255) | UNIQUE, NOT NULL, INDEX | Primary email address |
| `phone` | VARCHAR(50) | NULLABLE | Phone / WhatsApp number |
| `location` | VARCHAR(100) | NULLABLE | City / State / Country |
| `age` | INTEGER | NULLABLE | Client age |
| `role` | VARCHAR(50) | NOT NULL (DEFAULT 'USER') | SUPER_ADMIN, ADMIN, USER |
| `tier` | VARCHAR(50) | NOT NULL | License tier (e.g. USER_ANNUAL_365) |
| `is_active` | BOOLEAN | NOT NULL (DEFAULT TRUE) | Active status flag (killswitch) |
| `created_at` | DATETIME | NOT NULL | Record creation timestamp |
| `updated_at` | DATETIME | NOT NULL | Last update timestamp |

---

### 2.2 `licenses` Table
Stores issued cryptographic license tokens and expiration bounds.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | License record ID |
| `license_key` | VARCHAR(500) | UNIQUE, NOT NULL, INDEX | Cryptographic HMAC token |
| `key_type` | VARCHAR(50) | NOT NULL | SUPER_ADMIN_LIFETIME, USER_ANNUAL |
| `assigned_email` | VARCHAR(255) | NOT NULL, INDEX | Bound client email |
| `assigned_name` | VARCHAR(100) | NOT NULL | Bound client name |
| `is_valid` | BOOLEAN | NOT NULL (DEFAULT TRUE) | Validity status |
| `is_lifetime` | BOOLEAN | NOT NULL (DEFAULT FALSE) | Perpetual access flag |
| `issued_at` | DATETIME | NOT NULL | Date of issuance |
| `expires_at` | DATETIME | NULLABLE | Expiration date |

---

### 2.3 `memory_items` Table
Cognitive associative memory store for dynamic context recall.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Memory entry ID |
| `key` | VARCHAR(200) | UNIQUE, NOT NULL, INDEX | Associative keyword key |
| `content` | TEXT | NOT NULL | Stored fact / knowledge payload |
| `tags` | VARCHAR(500) | NULLABLE | Comma-separated search tags |
| `category` | VARCHAR(100) | NOT NULL, INDEX | IDENTITY, STEM, PREFERENCE, etc. |
| `importance` | INTEGER | NOT NULL (DEFAULT 1) | Retrieval ranking weight |
| `created_at` | DATETIME | NOT NULL | Creation timestamp |
| `updated_at` | DATETIME | NOT NULL | Last update timestamp |

---

### 2.4 `audit_logs` Table
Immutable security audit trail for zero-trust compliance.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Log entry ID |
| `event_type` | VARCHAR(100) | NOT NULL, INDEX | Event category |
| `severity` | VARCHAR(50) | NOT NULL (DEFAULT 'INFO') | INFO, WARNING, ERROR, CRITICAL |
| `actor` | VARCHAR(255) | NOT NULL | Operator / Process triggering event |
| `description` | TEXT | NOT NULL | Detailed event description |
| `ip_address` | VARCHAR(50) | NOT NULL | Origin IP address |
| `timestamp` | DATETIME | NOT NULL | Event timestamp |
