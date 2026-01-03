import reflex as rx

config = rx.Config(
    app_name="reflex_work_scheduler",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
    show_built_with_reflex = False
#    deploy_url='http://schedulemyshift.com',
#    api_url='http://18.221.203.137:8000'
)
