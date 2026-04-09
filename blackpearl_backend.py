


from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback
import key
from pubnub.models.consumer.v3.channel import Channel
from pubnub.models.consumer.v3.group import Group
from pubnub.models.consumer.v3.uuid import UUID
from queue import Queue
import hashlib


active_users = {}
msg_queue = Queue()
CHANNEL = "blackpearl"
usrcolor = {"zaz":"#0ec95f"}
pnconfig = None
pubnub = None
current_username = None

def assignusercolour(current_username):
 colours = hashlib.md5(current_username.encode()).hexdigest()[:6]
 usrcolor[current_username] = f"#{colours}"
 
def initialize_backend(authorized_uuid: str):
    global pnconfig, pubnub, current_username
    current_username = authorized_uuid.strip()

    pnconfig = PNConfiguration()
    pnconfig.publish_key = key.publish
    pnconfig.subscribe_key = key.subscribe
    pnconfig.secret_key = key.secret
    pnconfig.uuid = current_username

    pubnub = PubNub(pnconfig)

    # Token grant (same as before)
    channels = [Channel.id("blackpearl").read().write()]
    envelope = pubnub.grant_token() \
        .authorized_uuid(current_username) \
        .channels(channels) \
        .ttl(15) \
        .sync()

    pubnub.set_token(envelope.result.token.strip())

    class MySubscribeCallback(SubscribeCallback):
        def message(self, pubnub, message):
            data = message.message
            '''user = data.get('user')
            if user == current_username:
                return'''
            msg_queue.put(data)

        def presence(self, pubnub, presence):
            user = presence.uuid
            event = presence.event
            print(f"🔥 PRESENCE EVENT: {user} → {event}")

            if event == "join":
                active_users[user] = {"status": "online"}
            elif event in ["leave", "timeout"]:
                active_users.pop(user, None)
            elif event == "state-change" and presence.state:
                active_users[user] = {"status": presence.state.get("status", "online")}

            print(f"📋 Active users: {list(active_users.keys())}")

    pubnub.add_listener(MySubscribeCallback())
    pubnub.subscribe().channels(CHANNEL).with_presence().execute()

    

def send_message(msg: str):
    if pubnub and msg.strip():
        pubnub.publish().channel(CHANNEL).message({
            "user": current_username,
            "text": msg.strip()
        }).sync()


def set_user_status(status: str):
    if pubnub:
        pubnub.set_state().channels(CHANNEL).state({"status": status}).sync()
        if current_username in active_users:
            active_users[current_username]["status"] = status


def get_active_users():
    try:
        envelope = pubnub.here_now() \
            .channels(CHANNEL) \
            .include_uuids(True) \
            .include_state(True) \
            .sync()

        result = envelope.result
        if CHANNEL in result.channels:
            for occupant in result.channels[CHANNEL].occupants:
                u = occupant.uuid
                st = occupant.state or {}
                active_users[u] = {"status": st.get("status", "online")}
        print(f"📡 here_now returned {len(active_users)} users → {list(active_users.keys())}")
    except Exception as e:
        print(f"⚠️ here_now error: {e}")
    return active_users