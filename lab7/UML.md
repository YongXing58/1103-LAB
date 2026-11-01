# Lab 7 - UML Class Diagram

Notation used:

- `<<abstract>>` above a class name = abstract class. Abstract methods are marked `{abstract}`.
- `<<interface>>` above a class name = interface-style abstract base class.
- `-` private, `+` public.
- Inheritance / generalisation: **solid line, hollow triangle** pointing at the parent (`___|>`).
- Interface realisation: **dashed line, hollow triangle** pointing at the interface (`- - -|>`).
- Aggregation: hollow diamond at the whole (`<>`).

![Lab 7 UML class diagram](UML.png)

(`UML.svg` / `UML.png` - same diagram. Mermaid version below renders in GitHub / VS Code.)

```mermaid
classDiagram
    class CanBeShipped {
        <<interface>>
        +calculate_shipping_cost()* float
    }
    class Product {
        <<abstract>>
        -__product_id : str
        -__name : str
        -__price : float
        -__stock : int
        +__init__(product_id, name, price, stock)
        +get_product_id() str
        +get_name() str
        +get_price() float
        +get_stock() int
        +update_stock(quantity: int) bool
        +display_information() None
        +to_dict() dict
        +get_fulfilment_info()* str
    }
    class PhysicalProduct {
        +PRODUCT_TYPE : str = "physical"
        +BASE_SHIPPING_FEE : float = 5.00
        +COST_PER_KG : float = 2.50
        -__weight : float
        +__init__(product_id, name, price, stock, weight)
        +get_weight() float
        +display_information() None
        +get_fulfilment_info() str
        +calculate_shipping_cost() float
        +to_dict() dict
        +from_dict(data: dict)$ PhysicalProduct
    }
    class DigitalProduct {
        +PRODUCT_TYPE : str = "digital"
        -__download_size : float
        +__init__(product_id, name, price, stock, download_size)
        +get_download_size() float
        +display_information() None
        +get_fulfilment_info() str
        +to_dict() dict
        +from_dict(data: dict)$ DigitalProduct
    }
    class SubscriptionProduct {
        +PRODUCT_TYPE : str = "subscription"
        -__billing_months : int
        +__init__(product_id, name, price, stock, billing_months)
        +get_billing_months() int
        +display_information() None
        +get_fulfilment_info() str
        +to_dict() dict
        +from_dict(data: dict)$ SubscriptionProduct
    }
    class Inventory {
        -__products : List~Product~
        +add_product(product: Product) bool
        +search_product(product_id: str) Product
        +get_all_products() List~Product~
        +display_all() None
    }
    class InventoryFile {
        -__file_name : str
        +get_file_name() str
        +load() Inventory
        +save(inventory: Inventory) None
    }
    Product <|-- PhysicalProduct
    Product <|-- DigitalProduct
    Product <|-- SubscriptionProduct
    CanBeShipped <|.. PhysicalProduct
    Inventory "1" o-- "0..*" Product : has
    InventoryFile ..> Inventory : uses
```

Relationships (read as sentences):

| From                | To            | Relationship                         | Sentence                                         |
|---------------------|---------------|--------------------------------------|--------------------------------------------------|
| PhysicalProduct     | Product       | Inheritance (solid, hollow triangle)  | A physical product **is-a** product              |
| DigitalProduct      | Product       | Inheritance (solid, hollow triangle)  | A digital product **is-a** product               |
| SubscriptionProduct | Product       | Inheritance (solid, hollow triangle)  | A subscription product **is-a** product          |
| PhysicalProduct     | CanBeShipped  | Realisation (dashed, hollow triangle) | A physical product **must-be-able-to** be shipped |
| Inventory           | Product       | Aggregation 1 to 0..*                 | An inventory **has** zero or more products       |
| InventoryFile       | Inventory     | Dependency (uses)                     | InventoryFile **loads/saves** an inventory       |

`DigitalProduct` does **not** realise `CanBeShipped`, since digital products are never shipped.

`product_types.py` (the `PRODUCT_TYPES` registry) and `main.py` are modules, not classes, so they are
not drawn. `InventoryFile` uses the registry to rebuild the right subclass from the saved `"type"`.

## Responsibilities (SRP)

| Class / module       | Responsibility                                                     |
|----------------------|--------------------------------------------------------------------|
| Product (abstract)   | Common product data, stock management, common display / to_dict     |
| PhysicalProduct      | Weight, physical fulfilment, shipping cost                          |
| DigitalProduct       | Download size, digital fulfilment                                   |
| SubscriptionProduct  | Billing period, subscription fulfilment (optional task)             |
| CanBeShipped         | Contract: anything shippable must calculate a shipping cost         |
| Inventory            | Stores, adds, searches and displays products (any type)             |
| InventoryFile        | Loads and saves inventory data (JSON) with type identifiers         |
| product_types.py     | Maps a type identifier to its class, menu label and extra prompt    |
| main.py              | Displays the menu, gets input, calls the classes                    |
