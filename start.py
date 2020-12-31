import MySQLdb
import config
import time
import datetime
import requests

# create config
for device in config.devices:
    for user in config.devices[device].keys():
        config.devices[device][user]['send'] = 0
print("config was created...")


while 1 == 1:

    name  = []
    proto = []

    try:
        connection = MySQLdb.connect(host=config.db_host, db=config.db_base, user=config.db_user, passwd=config.db_pass, port=config.db_port)
        cursor = connection.cursor()
    except:
        print("   ERROR: Kein Verbindungsaufbau zur Datenbank, probiere es in 15 Sekunden erneut")
        time.sleep(15)
        continue
    
    cursor.execute(f"SELECT d.name,DATE_ADD(t.lastProtoDateTime, INTERVAL t.currentSleepTime SECOND) as proto FROM trs_status t LEFT JOIN settings_device d ON t.device_id = d.device_id WHERE t.instance_id = {config.instance_id} AND d.instance_id = {config.instance_id} ORDER BY t.lastProtoDateTime ASC, d.name ASC")

    all = list(cursor.fetchall())
    i = 0
    try:
        while i < len(all):
            name.append(all[i][0])
            proto.append(all[i][1])
            i +=1
    except:
        print("fehler")

    cursor = cursor.close()
    connection.close()

    worker = 0

    for device in config.devices:
        index = name.index(device)
        last_data = proto[index]

        last = datetime.datetime("1970-01-01 00:00:00").timestamp if last_data == None else datetime.datetime.strptime(str(last_data), '%Y-%m-%d %H:%M:%S').timestamp()
        now  = time.time()
        diff = now - last

        ################## MESSAGE #####################################################

        message_offine = "Dein Gerät <b>" + str(device) + "</b> ist Offline seit\n\u23F1 <code>" + str(last_data) + "</code>"
        message_online = "Super! Dein Gerät <b>" + str(device) + "</b> ist wieder Online \U0001F642"

        ################################################################################

        for user in config.devices[device].keys():
            if diff > config.timeout_sek:
                resend = now - config.devices[device][user]['send']
                if resend > config.new_send:
                    print("\n" + str(device) + ": detect timeout...")
                    now_timestamp = int(datetime.datetime.now().timestamp())
                    worker +=1
                    try:
                        requests.get(f'https://api.telegram.org/bot{config.token}/sendMessage?chat_id={user}&text={message_offine}&parse_mode=HTML')
                        print(" ==> send offline message to user_id: " + str(user))
                        config.devices[device][user]['send'] = now_timestamp
                    except:
                        print(" ==> offline message could not be sent to user_id: " + str(user))
            elif diff < config.timeout_sek and not config.devices[device][user]['send'] == 0:
                print("\n" + str(device) + ": is online again \U0001F642")
                worker +=1
                try:
                    requests.get(f'https://api.telegram.org/bot{config.token}/sendMessage?chat_id={user}&text={message_online}&parse_mode=HTML')
                    print(" ==> send online message to user_id: " + str(user))
                    config.devices[device][user]['send'] = 0
                except:
                    print(" ==> online message could not be sent to user_id: " + str(user))


    if worker == 0:
        print("nothing to do at time " + str(datetime.datetime.now().replace(microsecond=0)))
    
    #print(config.devices)
    time.sleep(config.sleeptime)