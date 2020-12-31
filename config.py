######################## CONFIG ########################

# Madmin
db_host = 'localhost'
db_user = 'user'
db_pass = 'pass'
db_base = 'mapadroid'
db_port = 3306

instance_id = 1     # madmin instance
timeout_sek = 1800  # seconds when a device is marked as offline     default 1800  (30 minutes)
sleeptime   = 300   # seconds when the data is updated               default  300  ( 5 minutes)
new_send    = 86400 # seconds to resend message to users             default 26400 (24h)

# Telegram
token   = '977638318:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

# config alerts
devices = {
  "atv01": {
    "1168486987": {},
    "645811038": {}
  },
  "atv02": {
    "645811038": {}
  },
  "atv03": {
    "645811038": {}
  },
  "atv04": {
    "645811038": {}
  }
}

########################################################

# The message can be adjusted in the middle of start.py!