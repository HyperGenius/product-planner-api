# routers/transaction/orders.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

# 作成したロジックと依存関係をインポート
from models.transaction.schedule import ScheduleRequest
from scheduler_logic import run_scheduler
from dependencies import get_order_repo, get_master_repo, get_schedule_repo
from repositories.supabase import (
    OrderRepository,
    MasterRepository,
    ScheduleRepository,
)

orders_router = APIRouter(prefix="/orders", tags=["Transaction (Orders)"])


@orders_router.post("/schedule")
async def create_schedule(
    req: ScheduleRequest,
    # Dependsを使ってリポジトリを注入
    order_repo: OrderRepository = Depends(get_order_repo),
    master_repo: MasterRepository = Depends(get_master_repo),
    schedule_repo: ScheduleRepository = Depends(get_schedule_repo),
):
    try:
        # ロジックにリポジトリを渡して実行
        return run_scheduler(req.order_id, order_repo, master_repo, schedule_repo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
