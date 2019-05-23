# coding: utf-8

import json

d = dict(a=1, b=3, c=2)

jd = json.dumps(d, sort_keys=True, indent=4)

print(jd)
