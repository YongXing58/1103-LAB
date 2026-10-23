# Lab 6 - UML Class Diagram

```
+---------------------------------------------+
|                   Product                   |
+---------------------------------------------+
| - __product_id : String                     |
| - __name : String                           |
| - __price : float                           |
| - __stock : int                             |
+---------------------------------------------+
| + __init__(product_id, name, price, stock)  |
| + get_product_id() : String                 |
| + get_name() : String                       |
| + get_price() : float                       |
| + get_stock() : int                         |
| + update_stock(quantity : int) : bool       |
| + display_information() : void              |
+---------------------------------------------+
                      ^
                      | 0..*
                      |
                      | 1
+---------------------------------------------+
|                  Inventory                  |
+---------------------------------------------+
| - __products : List<Product>                |
+---------------------------------------------+
| + __init__()                                |
| + add_product(product : Product) : bool     |
| + search_product(product_id : String)       |
|       : Product                             |
| + get_all_products() : List<Product>        |
| + display_all() : void                      |
+---------------------------------------------+
                      ^
                      | uses
                      |
+---------------------------------------------+
|                InventoryFile                |
+---------------------------------------------+
| - __file_name : String                      |
+---------------------------------------------+
| + __init__(file_name : String)              |
| + get_file_name() : String                  |
| + load() : Inventory                        |
| + save(inventory : Inventory) : void        |
+---------------------------------------------+
```

- An **Inventory** holds zero or more **Product** objects (aggregation).
- **InventoryFile** loads an Inventory from `inventory.json` and saves it back.
- **main.py** (the main program) shows the menu, gets user input and calls
  Inventory / Product / InventoryFile methods.

## Responsibilities (SRP)

| Class         | Responsibility                                   |
|---------------|--------------------------------------------------|
| Product       | Stores product information, manages its own stock |
| Inventory     | Stores, adds, searches and displays products     |
| InventoryFile | Loads and saves inventory data (JSON)            |
| main.py       | Displays the menu, gets input, calls the classes |
