import os
import requests
import urllib
import time

from datetime import datetime
from dateutil.relativedelta import relativedelta
from re import sub


# a few examples
sites = ['geocities.com','amazon.com','nytimes.com','yahoo.com']

# resource url
data_url = 'http://archive.org/wayback/available'


def _format(dt):
    return dt.strftime('%Y%m%d')


for item in sites:
    date = datetime(1990, 1, 1 )
    FIRST_RUN = True

    if not os.path.exists('images-'+item):
        os.mkdir('images-'+item)

    while date < datetime.now():
        obj = requests.get(data_url, params={'url':item,'timestamp':_format(date)})

        print date

        if hasattr(obj,'json') and obj.json().get('archived_snapshots',False):
            _url = obj.json()['archived_snapshots']['closest']['url']
            dt = obj.json()['archived_snapshots']['closest']['timestamp']

            # make url https to prevent webkit2png exception
            _url = sub(r'^http', 'https', _url)

            if FIRST_RUN:
                FIRST_RUN = False
                date = datetime.strptime(dt, '%Y%m%d%H%M%S')

            os.system("webkit2png {0} -o images-{2}/{1} -F --js=\"document.getElementById('wm-ipp').style.display='none';\"".format(_url,dt,item))
        else:
            print 'no snapshots found for ', date

        date += relativedelta(months=1)

        # be gentle
        time.sleep(0.5)

    os.system('python prepare.py {0} 1'.format('images-'+item))