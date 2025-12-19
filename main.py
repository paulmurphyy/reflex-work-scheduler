# main.py
import reflex as rx
from reflex_work_scheduler.reflex_work_scheduler import State
from reflex_work_scheduler.reflex_work_scheduler import index

app = rx.App()
# register states / pages
app.add_page(index)


# Export `app` for Gunicorn: `gunicorn -k uvicorn.workers.UvicornWorker main:app`
