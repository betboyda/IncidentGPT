# src/check_db.py

import sqlite3
import json
import os

# SQLite veritabanının yolu
# Analiz sonuçları burada tutuluyor
DB_PATH = os.path.join("db", "incident_history.db")

# Veritabanına bağlan
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Son eklenen 10 olayı çekiyoruz
# Amaç: sistem gerçekten kayıt alıyor mu görmek
cursor.execute("""
SELECT id, timestamp, incident_type, severity, is_multimodal, inference_time
FROM incidents
ORDER BY id DESC
LIMIT 10
""")

rows = cursor.fetchall()

print("\n=== SON 10 KAYIT ===\n")

# Kayıtları ekrana daha okunur şekilde yazdır
for r in rows:
    print(f"""
ID: {r[0]}
Time: {r[1]}
Incident Type: {r[2]}
Severity: {r[3]}
Multimodal: {'Yes' if r[4] else 'No'}
Inference Time: {r[5]} sec
------------------------
""")

# Veritabanı bağlantısını kapat
conn.close()
