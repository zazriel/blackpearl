from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback
import key
from pubnub.models.consumer.v3.channel import Channel
from queue import Queue
import hashlib

token = None
msg_queue = Queue()
CHANNEL = "blackpearl"
usrcolor = {}
pnconfig = None
pubnub = None
current_username = None
Password = {}

def assignusercolour(current_username):
 colours = hashlib.md5(current_username.encode()).hexdigest()[:6]
 usrcolor[current_username] = f"#{colours}"

def initialize_backend_pass(authorized_uuid: str): 
    global pnconfig, pubnub, current_username
    current_username = authorized_uuid.strip()
    
    pnconfig = PNConfiguration()
    pnconfig.publish_key = key.publish
    pnconfig.subscribe_key = key.subscribe
    pnconfig.secret_key = key.secret
    pnconfig.uuid = current_username

    pubnub = PubNub(pnconfig)

    
    
    
    token  = Password[current_username]["token"].strip()
    pubnub.set_token(token)

    class MySubscribeCallback(SubscribeCallback):
        def message(self, pubnub, message):
            data = message.message
            msg_queue.put(data)

        

    pubnub.add_listener(MySubscribeCallback())
    pubnub.subscribe().channels(CHANNEL).with_presence().execute()
 
def initialize_backend_token(authorized_uuid: str):
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
    
    
    token  = envelope.result.token.strip()
    pubnub.set_token(token)

    class MySubscribeCallback(SubscribeCallback):
        def message(self, pubnub, message):
            data = message.message
            msg_queue.put(data)

        

    pubnub.add_listener(MySubscribeCallback())
    pubnub.subscribe().channels(CHANNEL).with_presence().execute()
    return token
    

def send_message(msg: str):
    if pubnub and msg.strip():
        pubnub.publish().channel(CHANNEL).message({
            "user": current_username,
            "text": msg.strip()
        }).sync()




