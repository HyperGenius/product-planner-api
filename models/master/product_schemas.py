# models/master/product.py
from models.common.base_schema import BaseSchema
from pydantic import Field
from typing import Optional
from uuid import UUID


# --- Products ---
class ProductBase(BaseSchema):
    """製品のベーススキーマ"""

    name: str = Field(default=..., description="製品名")
    code: str = Field(default=..., description="製品コード")
    type: str = Field(default=..., description="製品種別")


class ProductCreateSchema(ProductBase):
    """製品を作成するためのスキーマ"""

    pass


class Product(ProductBase):
    """読み取り用製品のスキーマ"""

    id: int


class ProductUpdateSchema(BaseSchema):
    """製品を更新するためのスキーマ"""

    name: Optional[str] = Field(default=None, description="製品名")
    code: Optional[str] = Field(default=None, description="製品コード")
    type: Optional[str] = Field(default=None, description="製品種別")


# --- Process Routings ---
class RoutingCreate(BaseSchema):
    """製品の工程を新規作成するためのスキーマ"""

    product_id: int = Field(default=..., description="製品ID")
    sequence_order: int = Field(default=..., description="シーケンス番号")
    process_name: str = Field(default=..., description="工程名")
    equipment_group_id: int = Field(default=..., description="設備グループID")
    setup_time_seconds: int = Field(default=0, description="セットアップ時間")
    unit_time_seconds: float = Field(default=0, description="単位時間")
