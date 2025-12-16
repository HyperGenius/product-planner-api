# function_app.py
import os
import azure.functions as func
from fastapi import FastAPI
from supabase import create_client
from repositories.supabase import (
    OrderRepository,
    MasterRepository,
    ScheduleRepository,
)
from scheduler_logic import run_scheduler

# ルーターをインポート
from routers.transaction.orders import orders_router

# --- FastAPIのセットアップ ---
prod_planner_api = FastAPI(
    title="Product Planner API",
    description="API for product planning and scheduling using Supabase as the backend.",
    version="1.0.0",
)

# TODO: 例外ハンドラーの追加


# --- 各ルーターの登録 ---
prod_planner_api.include_router(orders_router)


@prod_planner_api.get("/")
async def root():
    return {"message": "Product Planner API"}


app = func.AsgiFunctionApp(
    app=prod_planner_api, http_auth_level=func.AuthLevel.FUNCTION
)
