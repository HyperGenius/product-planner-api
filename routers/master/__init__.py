# routers/master/__init__.py
from .products import product_router
from .equipments import equipment_router
from .equipment_groups import equipment_group_router

__all__ = [
    "product_router",
    "equipment_router",
    "equipment_group_router",
]
