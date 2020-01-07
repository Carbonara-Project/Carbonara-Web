import amqp_sender
import requests
import sys
import os
import hashlib
import asyncio

if len(sys.argv) < 2:
    print("usage: python task_test.py <path-to-file>\n")
    exit()

KEY="***"

name = os.path.basename(sys.argv[1])

print("Carbonara Analysis servers wake up...")
SERVERS_NUM = 8
async def wakeup():
    loop = asyncio.get_event_loop()
    futures = [
        loop.run_in_executor(
            None, 
            requests.get, 
            "https://carbonara-analysis-" + str(i) + ".herokuapp.com/"
        )
        for i in range(SERVERS_NUM)
    ]
    for response in await asyncio.gather(*futures):
        pass

loop = asyncio.get_event_loop()
loop.run_until_complete(wakeup())


print("Uploading binary on the file server...")
bin_file = open(sys.argv[1], "rb").read()

hash_md5 = hashlib.md5()
hash_md5.update(bin_file)
md5 = hash_md5.hexdigest()
print("md5: %s" % md5)

r = requests.post("https://carbonara-files.herokuapp.com/", params={"key":KEY}, files={"file":(md5, bin_file)})

print("Connecting to the task queque...")
s = amqp_sender.SenderAMQP()

url = "https://carbonara-files.herokuapp.com/" + md5 + "?key=" + KEY

s.send_task("777", name, url)
print("Task sended.")


