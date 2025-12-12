# Gunicorn configuration file
import multiprocessing

# Timeout for worker to process request (increased for AI calls)
timeout = 120  # 2 minutes - enough for AI processing

# Graceful timeout - time to wait for workers to finish before killing
graceful_timeout = 120

# Workers
workers = 2  # Render free tier has limited memory, keep it low
worker_class = 'sync'

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'

# Keep alive
keepalive = 5

# Preload app for faster worker startup
preload_app = True

