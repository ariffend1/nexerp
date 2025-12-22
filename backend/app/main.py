from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, products, manufacturing, procurement, sales, hr, finance, analytics, import_export, notifications, dashboards, currency_tax, ai, advanced_inventory, realtime, workflows, reports
from app.core.database import engine, Base
from app.models import auth as auth_models, inventory, accounting, ledger, manufacturing, procurement, sales, hr, journals, finance, notifications, rbac, currency_tax, ai_settings, advanced_inventory, workflow, reporting # Import metadata

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
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(products.router, prefix="/api/v1")
app.include_router(manufacturing.router, prefix="/api/v1")
app.include_router(procurement.router, prefix="/api/v1")
app.include_router(sales.router, prefix="/api/v1")
app.include_router(hr.router, prefix="/api/v1")
app.include_router(finance.router, prefix="/api/v1")
app.include_router(analytics.router, prefix="/api/v1")
app.include_router(import_export.router, prefix="/api/v1")
app.include_router(notifications.router, prefix="/api/v1")
app.include_router(dashboards.router, prefix="/api/v1")
app.include_router(currency_tax.router, prefix="/api/v1")
app.include_router(ai.router, prefix="/api/v1")
app.include_router(advanced_inventory.router, prefix="/api/v1")
app.include_router(realtime.router)
app.include_router(workflows.router, prefix="/api/v1")
app.include_router(reports.router, prefix="/api/v1")

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
