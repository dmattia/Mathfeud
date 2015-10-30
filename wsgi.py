#!/usr/bin/env python
import os
import sys
import site

sys.path.append('/mathfeud/mathfeud')
sys.path.append('/mathfeud/mathfeud/mathfeud')

os.environ['DJANGO_SETTINGS_MODULE'] = 'mathfeud.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mathfeud.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
