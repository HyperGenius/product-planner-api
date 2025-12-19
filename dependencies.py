# dependencies.py
import os
from supabase import create_client, Client
from repositories.supabase import (
    OrderRepository,
    ProductRepository,
    ScheduleRepository,
)

# Supabaseクライアントはアプリ全体で1つだけ作成（シングルトン）
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL:
    raise ValueError("SUPABASE_URL is not set")
if not SUPABASE_KEY:
    raise ValueError("SUPABASE_KEY is not set")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- Dependency Injection用の関数 ---


def get_order_repo() -> OrderRepository:
    """
    注文リポジトリを取得する。
    """
    return OrderRepository(supabase)


def get_schedule_repo() -> ScheduleRepository:
    """
    スケジュールリポジトリを取得する。
    """
    return ScheduleRepository(supabase)


def get_product_repo() -> ProductRepository:
    """
    プロダクトリポジトリを取得する。
    """
    return ProductRepository(supabase)
