# scheduler_logic.py
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Dict, Any
from repositories.supabase import (
    OrderRepository,
    MasterRepository,
    ScheduleRepository,
)


def run_scheduler(
    order_id: int,
    order_repo: OrderRepository,
    master_repo: MasterRepository,
    schedule_repo: ScheduleRepository,
) -> Dict[str, Any]:

    # --- 1. リポジトリ経由でデータ取得 ---
    order = order_repo.get_by_id(order_id)
    if not order:
        raise Exception("Order not found")
    if order.get("is_scheduled"):
        return {"message": "Already scheduled"}

    qty = order["quantity"]
    routings = master_repo.get_routings(order["product_id"])

    # 開始基準時間
    current_process_start = datetime.now().astimezone()
    created_count = 0

    # --- 2. 計算ロジック ---
    for routing in routings:
        group_id = routing["equipment_group_id"]

        # グループ内の設備ID一覧を取得
        machine_ids = master_repo.get_group_members(group_id)
        if not machine_ids:
            raise Exception(f"No machines in group {group_id}")

        # 空き枠探し
        candidates = []
        for mid in machine_ids:
            last_end = schedule_repo.get_last_end_time(mid)
            machine_free_at = last_end if last_end else datetime.now().astimezone()

            possible_start = max(machine_free_at, current_process_start)
            candidates.append({"mid": mid, "start": possible_start})

        # 最速の機械を選定
        best = min(candidates, key=lambda x: x["start"])

        # 所要時間計算 (Decimal対応)
        setup = routing.get("setup_time_seconds", 0) or 0
        unit = Decimal(str(routing["unit_time_seconds"]))
        total_sec = setup + (float(unit) * qty)

        end_time = best["start"] + timedelta(seconds=total_sec)

        # 保存
        new_schedule = {
            "order_id": order_id,
            "process_routing_id": routing["id"],
            "equipment_id": best["mid"],
            "start_datetime": best["start"].isoformat(),
            "end_datetime": end_time.isoformat(),
        }
        schedule_repo.create(new_schedule)
        created_count += 1

        current_process_start = end_time

    # --- 3. 完了更新 ---
    order_repo.mark_as_scheduled(order_id)

    return {"status": "success", "schedules_created": created_count}
