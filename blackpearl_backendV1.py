from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback
import key
from blackpearl_frontend import authorized_uuid
from pubnub.models.consumer.v3.channel import Channel
from pubnub.models.consumer.v3.group import Group
from pubnub.models.consumer.v3.uuid import UUID
from SSOP import *

active_users = {}
usr=[]


channels = [
    Channel.id("channel-a").read(),
    Channel.pattern("channel-[A-Za-z0-9]*").read(),
    Channel.id("channel-b").read().write(),
    Channel.id("channel-c").read().write(),
    Channel.id("blackpearl").read().write()
]
channel_groups = [
    Group.id("channel-group-b").read()
]
uuids = [
    UUID.id("uuid-c").get(),
    UUID.id("uuid-d").get().update()
]
pnconfig = PNConfiguration()
pnconfig.publish_key = key.publish
pnconfig.subscribe_key = key.subscribe

pnconfig.uuid = authorized_uuid.strip()

pubnub = PubNub(pnconfig)

envelope = pubnub.grant_token() \
    .authorized_uuid(authorized_uuid) \
    .channels(channels) \
    .groups(channel_groups) \
    .uuids(uuids) \
    .ttl(15) \
    .sync()

token = envelope.result.token
token_str = token.strip()

pubnub.set_token(token_str)

CHANNEL = "blackpearl"

class MySubscribeCallback(SubscribeCallback):
    def message(self, pubnub, message):
        data = message.message
        print(f"\n{data['user']}: {data['text']}")

    def status(self, pubnub, status):
        print("STATUS:", status.category)

    def presence(self, pubnub, presence):
        print(f"[PRESENCE] {presence.uuid} -> {presence.event}")
        user = presence.uuid

        if presence.event == "join":
            active_users[user] = "online"

        elif presence.event in ["leave", "timeout"]:
            active_users[user] = "offline"

        print("[ACTIVE USERS]", active_users)

pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels(CHANNEL).with_presence().execute()

print("✅ Connected! Start chatting:\n")

while True:
    try:
        msg = input("> ")
        pubnub.publish().channel(CHANNEL).message({         
            "user": pnconfig.user_id,      
            "text": msg,
            "type": "status",
            "user": pnconfig.user_id,
            "status": "online"
        }).sync()
       
    except Exception as e:
        print("Error:", e)