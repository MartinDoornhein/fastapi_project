from database import get_connection
from models.item import Item, ItemCreate


class ItemController:
    def list_items(self) -> list[Item]:
        with get_connection() as connection:
            rows = connection.execute(
                "SELECT id, name, description, price FROM items ORDER BY id"
            ).fetchall()
        return [
            Item(id=row[0], name=row[1], description=row[2], price=row[3])
            for row in rows
        ]

    def create_item(self, item_data: ItemCreate) -> Item:
        with get_connection() as connection:
            row = connection.execute(
                """
                INSERT INTO items (name, description, price)
                VALUES (%s, %s, %s)
                RETURNING id, name, description, price
                """,
                (item_data.name, item_data.description, item_data.price),
            ).fetchone()
        if row is None:
            raise RuntimeError("The database did not return the created item")
        return Item(id=row[0], name=row[1], description=row[2], price=row[3])


item_controller = ItemController()
