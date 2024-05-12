from django.urls import path
from . import views as V

urlpatterns = [
    path('insertTempData/', V.insertTempData, name='insertTempData'),
    path('tempdata/', V.tempData, name='tempData'),
    path('jsonShort/', V.jsonShort, name='jsonShort'),
    path('jsonLong/', V.jsonLong, name='jsonLong'),
    path('net/', V.net, name='net'),
    path('snmp/', V.snmp, name='snmp'),
    path('tx/', V.tx, name='tx'),
    path('ctc/', V.ctc, name='ctc'),
    path('sigPrc/', V.sigPrc, name='sigPrc'),
    path('pcs/', V.pcs, name='pcs'),
    path('adsb/', V.adsb, name='adsb'),
    path('operation/', V.operation, name='operation'),
]

