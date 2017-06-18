#!/usr/bin/env python3
from osmo_gsm_tester.test import *

hlr = suite.hlr()
bts = suite.bts()
mgcpgw = suite.mgcpgw(bts_ip=bts.remote_addr())
msc = suite.msc(hlr, mgcpgw)
bsc = suite.bsc(msc)
stp = suite.stp()
ms_mo = suite.modem()
ms_mt = suite.modem()

hlr.start()
stp.start()
msc.start()
mgcpgw.start()

bsc.bts_add(bts)
bsc.start()

bts.start()

hlr.subscriber_add(ms_mo)
hlr.subscriber_add(ms_mt)

ms_mo.connect(msc.mcc_mnc())
ms_mt.connect(msc.mcc_mnc())

ms_mo.log_info()
ms_mt.log_info()

print('waiting for modems to attach...')
wait(ms_mo.is_connected, msc.mcc_mnc())
wait(ms_mt.is_connected, msc.mcc_mnc())
wait(msc.subscriber_attached, ms_mo, ms_mt)

sms = ms_mo.sms_send(ms_mt)
wait(ms_mt.sms_was_received, sms)