"""
WSGI config for lamdataserver project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

# import sys
from django.core.wsgi import get_wsgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lamdataserver.settings')
os.environ["DJANGO_SETTINGS_MODULE"] = "lamdataserver.settings"
application = get_wsgi_application()

# print('END WSGI.PY')
# path = 'E:\1-program\11-LAMDataServer\lamdataserver'
# if path not in sys.path:
# 	sys.path.append(path)
# with open('log.txt','w+') as _f:
# 	_f.write('wsgi.py end\n')
