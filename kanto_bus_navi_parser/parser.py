# -*- coding: utf-8 -*-
import requests
from urllib.parse import urlencode
from lxml import html


class KantoBusNaviParser:
    BASE_URL = 'https://kanto-bus.bus-navigation.jp/wgsys/wgp/bus.htm?'
    MAX_ORDER = 10

    def search(self, to_busstop, from_busstop):
        """
        停留所名を指定してバス接近情報を検索する.
        :param to_busstop:
        :param from_busstop:
        :return:
        """
        param = {
            "bsid": '1',
            "toType": '1',
            "locale": 'ja',
            "tabName": 'searchTab',
            "from": from_busstop,
            "to": to_busstop,
            "mapFlag": 'false',
            "existYn": 'N'
        }
        qs = urlencode(param)
        url = self.__class__.BASE_URL + qs

        r = requests.get(url)

        tree = html.fromstring(r.content)

        results = []

        for num in range(1, self.__class__.MAX_ORDER):
            base_xpath = '/html/body/div[2]/div/div[4]/div/div[{}]/table/'.format(num)

            xpaths = {
                "route": base_xpath + 'tr[1]/td[1]/table/tr[1]/td/a/font',
                "destination": base_xpath + 'tr[1]/td[1]/table/tr[3]/td',
                "time_required": base_xpath + 'tr[1]/td[1]/table/tr[4]/td',
                "timetable": base_xpath + 'tr[1]/td[3]/div/table/tr[3]/td',
                "est_departure": base_xpath + 'tr[1]/td[3]/div/table/tr[4]/td',
                "est_arrival": base_xpath + 'tr[1]/td[4]/div/table/tr[4]/td',
                "condition": base_xpath + 'tr[2]/td[3]'
            }

            try:
                texts = {k: parser(tree, v) for k, v in xpaths.items()}
                results.append(texts)
            except:
                pass

        return results


def parser(tree, xpath):
    item = tree.xpath(xpath)

    if isinstance(item, list) and item:
        body = item[0].text_content()
    else:
        body = item.text_content()

    res = body.replace('\r\n', u'').replace('\t', u'').replace(u"\xa0", u'').replace(u'\u3000', u'').strip()

    return res
