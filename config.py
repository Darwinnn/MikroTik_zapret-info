# All parameters ARE MANDATORY.


# File paths

REQUEST_FILENAME = "files/request.xml"
SIGNATURE_FILENAME = "files/request.sig"
LOG_FILENAME = "zapret.log"
LASTDATEURGENT = "files/last_date_urgent"

# Attempts to request the XML from RSOC and the pause between them
# ATTEMPTS (default: 5) int
# ATTEMPT_TIME (default: 60) int seconds.

ATTEMPTS = 10
ATTEMPT_TIME = 120

# MikroTik NAS Servers where the DB will be uploaded to
# There can be as many servers as you want
# 
# str (IP or NS name): {
#    'login': str,
#    'port': int
# }

SERVERS = {
    '1.1.1.1': {
        'login': 'admin',
        'port': 22
    },
    '2.2.2.2': {
        'login': 'admin',
        'port': 22
    }
}
