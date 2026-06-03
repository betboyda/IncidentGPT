import sqlite3
import os
import json

from datetime import datetime

# ---------------------------------------------------
# DB PATH
# ---------------------------------------------------

DB_PATH = os.path.join(
    "db",
    "incident_history.db"
)

# ---------------------------------------------------
# INIT DB
# ---------------------------------------------------

def init_db():

    os.makedirs(
        "db",
        exist_ok=True
    )

    conn = sqlite3.connect(
        DB_PATH
    )

    cursor = conn.cursor()

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS incidents (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        timestamp TEXT,

        incident_type TEXT,

        severity TEXT,

        confidence_score INTEGER,

        raw_log TEXT,

        is_multimodal INTEGER,

        inference_time REAL,

        mitre_id TEXT,

        mitre_name TEXT,

        diagram_observations TEXT,

        actions TEXT
    )

    """)

    conn.commit()

    conn.close()

# ---------------------------------------------------
# SAVE INCIDENT
# ---------------------------------------------------

def save_incident(

    incident_type,

    severity,

    raw_log,

    is_multimodal,

    inference_time,

    diagram_observations,

    actions,

    confidence_score=0,

    mitre_id="Unknown",

    mitre_name="Unknown"
):

    conn = sqlite3.connect(
        DB_PATH
    )

    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO incidents (

        timestamp,

        incident_type,

        severity,

        confidence_score,

        raw_log,

        is_multimodal,

        inference_time,

        mitre_id,

        mitre_name,

        diagram_observations,

        actions

    )

    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

    """, (

        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        incident_type,

        severity,

        confidence_score,

        raw_log,

        int(is_multimodal),

        inference_time,

        mitre_id,

        mitre_name,

        json.dumps(
            diagram_observations,
            ensure_ascii=False
        ),

        json.dumps(
            actions,
            ensure_ascii=False
        )
    ))

    conn.commit()

    conn.close()

# ---------------------------------------------------
# GET ALL INCIDENTS
# ---------------------------------------------------

def get_all_incidents():

    conn = sqlite3.connect(
        DB_PATH
    )

    cursor = conn.cursor()

    cursor.execute("""

    SELECT *

    FROM incidents

    ORDER BY id DESC

    """)

    rows = cursor.fetchall()

    conn.close()

    return rows

# ---------------------------------------------------
# CLEAR DB
# ---------------------------------------------------

def clear_database():

    conn = sqlite3.connect(
        DB_PATH
    )

    cursor = conn.cursor()

    cursor.execute("""

    DELETE FROM incidents

    """)

    conn.commit()

    conn.close()