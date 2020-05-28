import os
import sys

#Calculate the path based on the location of the WSGI script.
apache_configuration= os.path.dirname(__file__)
project = os.path.dirname(apache_configuration)
workspace = os.path.dirname(project)

sys.path.append(project) #这个路径是项目主目录，如F:/mysite，一定要加上

os.environ['DJANGO_SETTINGS_MODULE'] = 'lamdataserver.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()