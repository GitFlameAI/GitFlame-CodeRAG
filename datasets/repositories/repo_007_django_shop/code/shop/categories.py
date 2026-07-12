from dataclasses import dataclass, field


@dataclass
class Category:
    id: int
    name: str
    product_ids: set[int] = field(default_factory=set)


def assign_product(category: Category, product_id: int) -> None:
    category.product_ids.add(product_id)


def products_in_category(category: Category, catalog: dict) -> list[dict]:
    return [vars(catalog[pid]) for pid in category.product_ids if pid in catalog]
