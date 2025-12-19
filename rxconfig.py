import reflex as rx

config = rx.Config(
    app_name="reflex_work_scheduler",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)