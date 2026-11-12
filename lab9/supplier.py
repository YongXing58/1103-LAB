class Supplier:
    # Responsibility: represent a supplier of products.
    # A Supplier is created independently and then given to a Product
    # (association: the product only knows about its supplier).

    def __init__(self, supplier_id: str, name: str, contact_email: str):
        self.supplier_id: str = supplier_id
        self.name: str = name
        self.contact_email: str = contact_email

    def display_information(self) -> None:
        print("Supplier: " + self.supplier_id
              + " | Name: " + self.name
              + " | Email: " + self.contact_email)

    def to_dict(self) -> dict:
        return {
            "supplier_id": self.supplier_id,
            "name": self.name,
            "contact_email": self.contact_email
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Supplier":
        return cls(data["supplier_id"], data["name"], data["contact_email"])
