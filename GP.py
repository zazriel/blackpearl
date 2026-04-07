from pubnub.models.consumer.v3.channel import Channel
from pubnub.models.consumer.v3.group import Group
from pubnub.models.consumer.v3.uuid import UUID
from SSOP import *
usr = []
authorized_uuid = input("Enter the username/uuid to authorize this token for: ")
usr.append(authorized_uuid)
print(usr)
print(authorized_uuid)

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


print(token)
