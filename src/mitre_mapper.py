# src/mitre_mapper.py

MITRE_MAP = {

    "brute_force_attack": {
        "id": "T1110",
        "name": "Brute Force"
    },

    "phishing": {
        "id": "T1566",
        "name": "Phishing"
    },

    "malware_activity": {
        "id": "T1204",
        "name": "User Execution"
    },

    "network_attack": {
        "id": "T1498",
        "name": "Network Denial of Service"
    },

    "authentication_attack": {
        "id": "T1078",
        "name": "Valid Accounts"
    }
}


def map_to_mitre(incident_type: str):

    return MITRE_MAP.get(
        incident_type,
        {
            "id": "Unknown",
            "name": "Unknown Technique"
        }
    )