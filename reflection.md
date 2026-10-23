# Lab 6 - Reflection Questions

**1. What is the difference between a class and an object?**
A class is a blueprint that defines what attributes and methods something has. An object is an actual instance created from that blueprint with its own values. `Product` is the class; `Product("P001", "Laptop", 1200.00, 15)` is an object.

**2. Why is Product a suitable class for this system?**
Products are the main "thing" the inventory system deals with. Each one has its own data (ID, name, price, stock) and its own behaviour (updating stock, displaying itself), so it makes sense to group them together in one class.

**3. What data belongs inside a Product object?**
The product ID, name, price and stock quantity.

**4. Why should the Product class manage its own stock rather than the main program directly changing it?**
If stock is only changed through `update_stock()`, the Product can check the value first (e.g. reject negative numbers or non-integers). If the main program changed it directly, any part of the code could put the product into an invalid state and there would be no single place to enforce the rules.

**5. What does encapsulation mean in your program?**
The Product's attributes are private (`__product_id`, `__name`, `__price`, `__stock`) and other code only reads them through getters and changes stock through `update_stock()`. Likewise, Inventory keeps its list of products private and only exposes methods like `add_product()` and `search_product()`, and `get_all_products()` returns a copy of the list.

**6. What is the responsibility of the Product class?**
To represent and manage a single product: store its information and manage its own state (stock).

**7. What is the responsibility of the Inventory class?**
To manage a collection of Product objects: store them, add new ones (without duplicate IDs), search by ID and display them all.

**8. How does separating these responsibilities demonstrate the Single Responsibility Principle?**
Each class has one reason to change. If the way a product validates stock changes, only `Product` changes. If the way products are stored or searched changes, only `Inventory` changes. If the file format changes, only `InventoryFile` changes. The menu and user input stay in the main program.

**9. What information does the main program need to know about a Product?**
Only its public interface: how to create one (`Product(id, name, price, stock)`), how to read its details (`get_name()`, `get_stock()` etc.), how to change its stock (`update_stock()`) and how to display it (`display_information()`).

**10. What information about the internal implementation of Product does the main program not need to know?**
How the attributes are named and stored (the private `__` attributes and name mangling), how stock validation is done inside `update_stock()`, and how `display_information()` formats the output. The main program also doesn't need to know how products are converted to/from JSON, which is handled by `InventoryFile`.
