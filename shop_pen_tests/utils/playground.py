from pydantic import ValidationError

from modino_tests.sdk.net.modino_api_client import ModinoClient
from modino_tests.sdk.net.rest_client import RestClient, RestConfigFromCfg
from modino_tests.sdk.base.config import GeneralConfigParser
import random
from modinoapi.models.mug import Mug

cfg = GeneralConfigParser()
cfg.read_conf_file("localhost.conf")

# step by step
rest_config = RestConfigFromCfg()
rest_config.set_properties(cfg['SHOPEN'])
rest_client = RestClient(rest_config)

# simple create
client = ModinoClient(cfg['SHOPEN'])
client.authorization_oidc()

# mugs = client.mug.list_mugs()
# for _m in mugs['content']:
#     print(f'->{_m["name"]}->{_m}')
#     client.mug.delete_mug(_m["id"])
# try:
#     mug = client.mug.create_mug({"name": f'SOmeTest {random.randint(1, 1000)}'})
#     print(mug)
#     m = Mug.from_dict(mug)
#     client.mug.get_mug(m.id)
#     client.mug.delete_mug(m.id)
# except ValidationError as _exp:
#     print([f'-->{i["msg"]}' for i in _exp.errors()])
# client.mug.get_mug(mug["id"])
# client.mug.delete_mug(mug["id"])
