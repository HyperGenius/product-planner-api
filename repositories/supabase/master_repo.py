# repositories/supabase/master_repo.py
from supabase import Client
from typing import List, Dict, Any
from .table_name import SupabaseTableName


class MasterRepository:
    """マスタデータを管理するリポジトリクラス。"""

    def __init__(self, client: Client):
        self.client = client

    def get_routings(self, product_id: int) -> List[Dict[str, Any]]:
        """指定された製品IDに関連する工程ルーティングのリストを取得する。
        Args:
            product_id (int): 製品の一意の識別子。

        Returns:
            List[Dict[str, Any]]: 工程ルーティングのリスト。各要素は工程ルーティングのデータを含む辞書。
        """
        res = (
            self.client.table(SupabaseTableName.PROCESS_ROUTINGS.value)
            .select("*")
            .eq("product_id", product_id)
            .order("sequence_order")
            .execute()
        )
        return res.data or []

    def get_group_members(self, group_id: int) -> List[int]:
        """指定された設備グループIDに関連する設備IDのリストを取得する。

        Args:
            group_id (int): 設備グループの一意の識別子。

        Returns:
            List[int]: 設備IDのリスト。
        """
        res = (
            self.client.table(SupabaseTableName.EQUIPMENT_GROUP_MEMBERS.value)
            .select("equipment_id")
            .eq("equipment_group_id", group_id)
            .execute()
        )
        return [item["equipment_id"] for item in res.data]
