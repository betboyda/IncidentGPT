import re
from collections import Counter

# ---------------------------------------------------
# STRUCTURED LOG PARSER
# ---------------------------------------------------

def parse_log(log_text: str):

    parsed_logs = []

    lines = log_text.splitlines()

    pattern = (
        r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+'
        r'(\S+)\s+'
        r'user=(\S+)\s+'
        r'ip=(\S+)'
    )

    for line in lines:

        match = re.search(
            pattern,
            line
        )

        if match:

            parsed_logs.append({

                "timestamp": match.group(1),

                "event_type": match.group(2),

                "user": match.group(3),

                "ip": match.group(4)
            })

        else:

            # ---------------------------------------------------
            # GENERIC FALLBACK PARSER
            # ---------------------------------------------------

            generic_ip = re.search(
                r'(\d+\.\d+\.\d+\.\d+)',
                line
            )

            generic_user = re.search(
                r'user[:= ](\S+)',
                line,
                re.IGNORECASE
            )

            event_type = "UNKNOWN"

            upper_line = line.upper()

            if "LOGIN_FAILED" in upper_line:

                event_type = (
                    "LOGIN_FAILED"
                )

            elif "LOGIN_SUCCESS" in upper_line:

                event_type = (
                    "LOGIN_SUCCESS"
                )

            elif "PHISHING" in upper_line:

                event_type = (
                    "PHISHING_ALERT"
                )

            elif "MALWARE" in upper_line:

                event_type = (
                    "MALWARE_ALERT"
                )

            elif "DDOS" in upper_line:

                event_type = (
                    "DDOS_ALERT"
                )

            parsed_logs.append({

                "timestamp": "UNKNOWN",

                "event_type": event_type,

                "user": (
                    generic_user.group(1)
                    if generic_user
                    else "unknown"
                ),

                "ip": (
                    generic_ip.group(1)
                    if generic_ip
                    else "unknown"
                )
            })

    return parsed_logs

# ---------------------------------------------------
# BRUTE FORCE DETECTION
# ---------------------------------------------------

def detect_brute_force(
    parsed_logs
):

    failed_attempts = Counter()

    for log in parsed_logs:

        if (
            log["event_type"]
            == "LOGIN_FAILED"
        ):

            ip = log["ip"]

            failed_attempts[ip] += 1

    suspicious_ips = []

    for ip, count in failed_attempts.items():

        if count >= 3:

            suspicious_ips.append({

                "ip": ip,

                "attempts": count,

                "attack_type": (
                    "brute_force"
                )
            })

    return suspicious_ips

# ---------------------------------------------------
# PHISHING DETECTION
# ---------------------------------------------------

def detect_phishing(
    parsed_logs
):

    phishing_events = []

    for log in parsed_logs:

        if (
            "PHISHING"
            in log["event_type"]
        ):

            phishing_events.append(log)

    return phishing_events

# ---------------------------------------------------
# MALWARE DETECTION
# ---------------------------------------------------

def detect_malware(
    parsed_logs
):

    malware_events = []

    for log in parsed_logs:

        if (
            "MALWARE"
            in log["event_type"]
        ):

            malware_events.append(log)

    return malware_events

# ---------------------------------------------------
# NETWORK ATTACK DETECTION
# ---------------------------------------------------

def detect_network_attack(
    parsed_logs
):

    network_events = []

    for log in parsed_logs:

        if (
            "DDOS"
            in log["event_type"]
        ):

            network_events.append(log)

    return network_events

# ---------------------------------------------------
# INCIDENT CORRELATION
# ---------------------------------------------------

def correlate_events(
    parsed_logs
):

    correlations = []

    brute_force = detect_brute_force(
        parsed_logs
    )

    phishing = detect_phishing(
        parsed_logs
    )

    malware = detect_malware(
        parsed_logs
    )

    network = detect_network_attack(
        parsed_logs
    )

    if brute_force:

        correlations.append({

            "type": (
                "Brute Force Attack"
            ),

            "count": len(
                brute_force
            )
        })

    if phishing:

        correlations.append({

            "type": "Phishing",

            "count": len(
                phishing
            )
        })

    if malware:

        correlations.append({

            "type": "Malware",

            "count": len(
                malware
            )
        })

    if network:

        correlations.append({

            "type": (
                "Network Attack"
            ),

            "count": len(
                network
            )
        })

    return correlations