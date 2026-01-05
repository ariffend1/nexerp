from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# API Routers
from app.api import auth as auth_api
from app.api import products as products_api
from app.api import manufacturing as manufacturing_api
from app.api import procurement as procurement_api
from app.api import sales as sales_api
from app.api import hr as hr_api
from app.api import finance as finance_api
from app.api import analytics as analytics_api
from app.api import import_export as import_export_api
from app.api import notifications as notifications_api
from app.api import dashboards as dashboards_api
from app.api import currency_tax as currency_tax_api
from app.api import reports as reports_api
# DISABLED ADVANCED API MODULES:
# from app.api import ai, advanced_inventory, realtime, workflows

from app.core.database import engine, Base
# Model Imports for table creation
from app.models import auth as auth_models
from app.models import inventory, accounting, ledger
from app.models import manufacturing as manufacturing_models
from app.models import procurement as procurement_models
from app.models import sales as sales_models
from app.models import hr as hr_models
from app.models import journals, finance as finance_models
from app.models import notifications as notifications_models
from app.models import rbac, currency_tax as currency_tax_models
from app.models import reporting
# DISABLED ADVANCED MODELS:
# from app.models import ai_settings, advanced_inventory, workflow

# Initialize Database
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="NexERP API",
    description="Backend API for NexERP - Modern Manufacturing & Service ERP",
    version="0.1.0"
)

# Configure CORS
origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:8000",
    "http://localhost:8001",
    "http://192.168.5.13:3000",  # Proxmox Production
    "http://192.168.5.13:3001",
    "http://192.168.5.13:8000",
    "http://192.168.5.13:8001",
    "http://192.168.5.14:3000",  # Proxmox Alt
    "http://192.168.5.14:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Core API Routers
app.include_router(auth_api.router, prefix="/api/v1")
app.include_router(products_api.router, prefix="/api/v1")
app.include_router(manufacturing_api.router, prefix="/api/v1")
app.include_router(procurement_api.router, prefix="/api/v1")
app.include_router(sales_api.router, prefix="/api/v1")
app.include_router(hr_api.router, prefix="/api/v1")
app.include_router(finance_api.router, prefix="/api/v1")
app.include_router(analytics_api.router, prefix="/api/v1")
app.include_router(import_export_api.router, prefix="/api/v1")
app.include_router(notifications_api.router, prefix="/api/v1")
app.include_router(dashboards_api.router, prefix="/api/v1")
app.include_router(currency_tax_api.router, prefix="/api/v1")
app.include_router(reports_api.router, prefix="/api/v1")

# DISABLED ADVANCED MODULES:
# app.include_router(ai.router, prefix="/api/v1")
# app.include_router(advanced_inventory.router, prefix="/api/v1")
# app.include_router(realtime.router)
# app.include_router(workflows.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "app": "NexERP API",
        "status": "online",
        "version": "0.1.0",
        "documentation": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
