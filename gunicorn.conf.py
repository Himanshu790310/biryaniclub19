# Gunicorn configuration file
import multiprocessing

# Server socket
bind = "127.0.0.1:8000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync'
worker_connections = 1000
timeout = 120
keepalive = 2

# Process naming
proc_name = 'biryaniclub'

# Logging
accesslog = '/var/log/biryaniclub/access.log'
errorlog = '/var/log/biryaniclub/error.log'
loglevel = 'info'

# Process management
daemon = False
pidfile = '/var/run/biryaniclub/gunicorn.pid'
umask = 0
user = 'biryaniclub'
group = 'biryaniclub'

# SSL (uncomment if using SSL)
# keyfile = '/etc/ssl/private/biryaniclub.key'
# certfile = '/etc/ssl/certs/biryaniclub.crt'

# Server mechanics
preload_app = True
reload = False
spew = False

# Server hooks
def on_starting(server):
    pass

def on_reload(server):
    pass

def when_ready(server):
    pass

def on_exit(server):
    pass
