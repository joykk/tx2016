#!/usr/bin/env python
# -*- coding: utf-8 -*-

from handlers import ChinaTop20Handler,ChinaAllSecHandler,ChinarealSumHandler,ChinaCurrentSumHandler,ChinaSecHandler,ProviceSumHandler,ChinaSecondSumHandler, ChinaHandler, ProviceHandler, Top3Handler,Top3DetailHandler, ChinaMinSumHandler

url_patterns = [(r"/province_min/([0-9]*)", ChinaHandler),
                (r"/city_min/([0-9]*)", ProviceHandler),
                (r"/top3/([0-9]*)", Top3Handler),
                (r"/top3detail/([0-9]*)", Top3DetailHandler),
                (r"/china_sec/([0-9]*)", ChinaSecondSumHandler),
                (r"/china_min/([0-9]*)", ChinaMinSumHandler),
                (r"/province_sec_sum/([0-9]*)/([0-9]*)", ProviceSumHandler),
                (r"/province_sec/([0-9]*)" , ChinaSecHandler),
                (r"/china_all/([0-9]*)" , ChinaCurrentSumHandler),
                (r"/china_real/([0-9]*)", ChinarealSumHandler),
                (r"/china_sec_num/([0-9]*)", ChinaAllSecHandler),
                (r"/china_top10/([0-9]*)" , ChinaTop20Handler)
                ]
