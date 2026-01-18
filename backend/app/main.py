# backend/main.py
from fastapi import FastAPI

from app.routers.master import (
    equipment_group_router,
    equipment_router,
    process_routing_router,
    product_router,
)
from app.routers.transaction import orders_router

# FastAPIアプリの初期化
product_planner_api = FastAPI(
    title="Product Planner API",
    description="API on Render",
    version="1.0.0",
)

# ルーターの登録
product_planner_api.include_router(product_router)
product_planner_api.include_router(equipment_router)
product_planner_api.include_router(equipment_group_router)
product_planner_api.include_router(process_routing_router)
product_planner_api.include_router(orders_router)


@product_planner_api.get("/health")
async def health():
    return {"status": "ok", "platform": "Render"}
