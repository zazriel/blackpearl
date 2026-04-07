from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
import key

pn_config = PNConfiguration()
pn_config.subscribe_key = key.subscribe
pn_config.publish_key = key.publish
pn_config.secret_key = key.secret
pn_config.uuid = "uuid-c"  # This can be any string, but should match the authorized UUID in the token
pubnub = PubNub(pn_config)



