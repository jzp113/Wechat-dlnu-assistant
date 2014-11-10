#!/usr/bin/env python
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from app import app
app.run(host = '10.146.110.111',debug = True)
