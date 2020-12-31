### this script sends the user a message that the device is offline. Different users can be specified for each device

## Config
config the `config.py` file with your data
the heart of the script is the config json with the following structure. here's an example: (the key ist your device in Madmin and the id the Userids of Telegram Users)
```
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
```

## Start
`python3 start.py`


## Notes

Limits on Telegram Channels are 30 Messages per second and for Groups 20 messages per minute
