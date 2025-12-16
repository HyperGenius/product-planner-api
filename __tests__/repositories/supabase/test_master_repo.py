# __tests__/repositories/supabase/test_master_repo.py
import pytest
from unittest.mock import MagicMock
from typing import Any

# テスト対象のクラスをインポート
from repositories.supabase.master_repo import MasterRepository
from repositories.supabase.table_name import SupabaseTableName


class TestMasterRepository:
    """MasterRepositoryの単体テストクラス"""

    @pytest.fixture
    def mock_client(self):
        """Supabase Clientのモックを作成するフィクスチャ"""
        return MagicMock()

    @pytest.fixture
    def repo(self, mock_client):
        """MasterRepositoryのインスタンスを作成するフィクスチャ"""
        return MasterRepository(mock_client)

    def test_get_routings_success(self, repo, mock_client):
        """get_routings: データが取得できた場合の正常系テスト"""
        # 1. 準備
        product_id = 100
        expected_data = [
            {"id": 1, "process_name": "Cut", "sequence_order": 1},
            {"id": 2, "process_name": "Assemble", "sequence_order": 2},
        ]

        # 2. モックの振る舞いを定義 (メソッドチェーンをモック化)
        # client.table().select().eq().order().execute().data = expected_data
        (
            mock_client.table.return_value.select.return_value.eq.return_value.order.return_value.execute.return_value.data
        ) = expected_data

        # 3. 実行
        result = repo.get_routings(product_id)

        # 4. 検証
        assert result == expected_data

        # 呼び出し引数の検証
        mock_client.table.assert_called_with(SupabaseTableName.PROCESS_ROUTINGS.value)
        mock_client.table.return_value.select.assert_called_with("*")
        mock_client.table.return_value.select.return_value.eq.assert_called_with(
            "product_id", product_id
        )
        mock_client.table.return_value.select.return_value.eq.return_value.order.assert_called_with(
            "sequence_order"
        )

    def test_get_routings_empty(self, repo, mock_client):
        """get_routings: データが存在しない場合(Noneまたは空リスト)のテスト"""
        # 1. 準備
        product_id = 999

        # execute().data が None を返すケース（ Supabase clientの挙動による）
        (
            mock_client.table.return_value.select.return_value.eq.return_value.order.return_value.execute.return_value.data
        ) = None  # または []

        # 2. 実行
        result = repo.get_routings(product_id)

        # 3. 検証 (Noneの場合は空リスト [] に変換されていること)
        assert result == []

    def test_get_group_members_success(self, repo, mock_client):
        """get_group_members: 設備IDリストが正しく抽出されるかのテスト"""
        # 1. 準備
        group_id = 10
        # DBからは辞書のリストが返ってくる想定
        db_response_data = [
            {"equipment_id": 101},
            {"equipment_id": 102},
            {"equipment_id": 103},
        ]
        # メソッドの戻り値はIDのリストになるはず
        expected_result = [101, 102, 103]

        # 2. モックの振る舞いを定義
        # client.table().select().eq().execute().data
        (
            mock_client.table.return_value.select.return_value.eq.return_value.execute.return_value.data
        ) = db_response_data

        # 3. 実行
        result = repo.get_group_members(group_id)

        # 4. 検証
        assert result == expected_result

        # 呼び出し引数の検証
        mock_client.table.assert_called_with(
            SupabaseTableName.EQUIPMENT_GROUP_MEMBERS.value
        )
        mock_client.table.return_value.select.assert_called_with("equipment_id")
        mock_client.table.return_value.select.return_value.eq.assert_called_with(
            "equipment_group_id", group_id
        )

    def test_get_group_members_empty(self, repo, mock_client):
        """get_group_members: メンバーがいない場合のテスト"""
        # 1. 準備
        group_id = 99

        (
            mock_client.table.return_value.select.return_value.eq.return_value.execute.return_value.data
        ) = []

        # 2. 実行
        result = repo.get_group_members(group_id)

        # 3. 検証
        assert result == []
