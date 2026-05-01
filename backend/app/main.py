from fastapi import FastAPI
from app.api import alerts,incidents,assets,detections,playbooks,metrics,reports,audit,health
app=FastAPI()
for r in [alerts.router,incidents.router,assets.router,detections.router,playbooks.router,metrics.router,reports.router,audit.router,health.router]:
 app.include_router(r,prefix="/api")
