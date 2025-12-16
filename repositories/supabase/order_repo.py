# repositories/supabase/order_repo.py
from supabase import Client
from typing import Optional, Dict, Any


class OrderRepository:
    def __init__(self, client: Client):
        self.client = client

    def get_by_id(self, order_id: int) -> Optional[Dict[str, Any]]:
        """
        IDで単一の注文を取得する。

        Args:
            order_id (int): 取得する注文の一意の識別子。

        Returns:
            Optional[Dict[str, Any]]: 注文が見つかった場合は注文データを含む辞書、
                                      注文が存在しない場合はNone。

        Raises:
            APIError: Supabase APIリクエストが失敗した場合。
        """
        res = (
            self.client.table("orders")
            .select("*")
            .eq("id", order_id)
            .single()
            .execute()
        )
        return res.data

    def mark_as_scheduled(self, order_id: int) -> None:
        """
        注文をスケジュール済みとしてマークする。

        Args:
            order_id (int): スケジュール済みとしてマークする注文の一意の識別子。

        Raises:
            APIError: Supabase APIリクエストが失敗した場合。
        """
        self.client.table("orders").update({"is_scheduled": True}).eq(
            "id", order_id
        ).execute()
