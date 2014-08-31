#!/bin/bash
set -e
## Root
#su - ;

# gunicorn djdam.wsgi:application --bind=127.0.0.1:9000 --name "djdam" \
# --workers 5 --user=www-data --group=www-data --log-level=debug &  \
# nginx -p /home/johnb/virtualenvs/DJDAM/src/djdam/ -c /home/johnb/virtualenvs/DJDAM/src/djdam/conf/nginx.conf


export NAME="djdam_nginx" # Name of the application
export DJANGODIR=/home/johnb/vm/djangodam/src/ # Django project directory
export PYTHONDIR=/home/johnb/vm/djangodam/bin/ # Django project directory
export SOCKFILE=$DJANGODIR/var/run/gunicorn.sock # we will communicte using this unix socket
export LOGFILE=$DJANGODIR/var/log/gunicorn/searcher.log
export LOGDIR=$(dirname $LOGFILE)
export USER=www-data # the user to run as
export GROUP=www-data # the group to run as
export NUM_WORKERS=5 # how many worker processes should Gunicorn spawn
export DJANGO_SETTINGS_MODULE=djdam.settings #.local # which settings file should Django use
export DJANGO_WSGI_MODULE=djdam.wsgi # WSGI module name

echo "Starting $NAME"

# Activate the virtual environment
cd $DJANGODIR
source ../bin/activate

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

## Add Needed files to PATH
export PYTHONPATH=$DJANGODIR:$DJANGODIR/settings:$DJANGODIR/apps:$DJANGODIR/../../src:$DJANGODIR/../../bin:$PYTHONPATH

## Start Guni
#$PYTHONDIR/gunicorn djdam.wsgi:application --bind=127.0.0.1:9000 --name $NAME --workers $NUM_WORKERS --user=$USER --group=$GROUP --log-level=debug &

## Start Nginx
/usr/sbin/nginx -p ${DJANGODIR} -c ${DJANGODIR}/conf/nginx.conf &



# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
#exec ../../bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
#--name $NAME \
#--workers $NUM_WORKERS \
#--user=$USER --group=$GROUP \
#--log-level=debug \
#--log-file=$LOGFILE 2>>$LOGFILE \
#--bind=127.0.0.1:9000
# --bind=unix:$SOCKFILE

#echo "Mid $NAME"

## Start nginx rev-Proxy to Route django reqs and serve Static files
# DJANGODIR=/home/johnb/virtualenvs/DJDAM/src/djdam/ # Django project directory
#nginx \
#--prefix ${DJANGODIR}/ \
#--config conf/nginx.conf

echo "End Starting $NAME"
