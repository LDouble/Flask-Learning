import  os
from  gevent import monkey
monkey.patch_all()
import multiprocessing

debug = False
bind = "0.0.0.0:5001"
pidfile = "gunicorn.pid"
logfile = "error.log"
workers = multiprocessing.cpu_count()*2 + 1
worker_class = "gevent"
daemon = True
