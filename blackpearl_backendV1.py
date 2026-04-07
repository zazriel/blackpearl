from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback
import key

from pubnub.models.consumer.v3.channel import Channel
from pubnub.models.consumer.v3.group import Group
from pubnub.models.consumer.v3.uuid import UUID
from SSOP import *

active_users = {}
usr=[]
authorized_uuid = input("Enter the username/uuid to authorize this token for: ")
usr.append(authorized_uuid)

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
envelope = pubnub.grant_token() \
    .authorized_uuid(authorized_uuid) \
    .channels(channels) \
    .groups(channel_groups) \
    .uuids(uuids) \
    .ttl(15) \
    .sync()

token = envelope.result.token

pnconfig = PNConfiguration()
pnconfig.publish_key = key.publish
pnconfig.subscribe_key = key.subscribe

pnconfig.uuid = authorized_uuid.strip()

token_str = token.strip()

pubnub = PubNub(pnconfig)

pubnub.set_token(token_str)

CHANNEL = "blackpearl"

class MySubscribeCallback(SubscribeCallback):
    def message(self, pubnub, message):
        data = message.message
        print(f"\n{data['user']}: {data['text']}")

    def status(self, pubnub, status):
        print("STATUS:", status.category)

pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels(CHANNEL).with_presence().execute()

print("✅ Connected! Start chatting:\n")

while True:
    try:
        msg = input("> ")
        pubnub.publish().channel(CHANNEL).message({
            "user": pnconfig.user_id,      
            "text": msg
        }).sync()
    except Exception as e:
        print("Error:", e)