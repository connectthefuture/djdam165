#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    ## Add Html Tidy Debug panel to syspat
    sys.path.append(os.path.join((os.path.dirname(os.path.dirname(__file__)),'local/debug_toolbar_htmltidy' )))
    #sys.path.append(os.path.abspath('/home/johnb/virtualenvs/DJDAM/local/debug_toolbar_html'))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djdam.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
