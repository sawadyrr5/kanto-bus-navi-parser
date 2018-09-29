# -*- coding: utf-8 -*-
from kanto_bus_navi_parser.parser import KantoBusNaviParser

mybus = KantoBusNaviParser()

p = mybus.search(from_busstop='中野駅', to_busstop='練馬駅')
print(p)
