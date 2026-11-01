# Lab 7 - Inventory Management System (Inheritance, Overriding, Abstract, Interfaces)

## Files

| File                      | Contents                                                        |
|---------------------------|-----------------------------------------------------------------|
| `product.py`              | `Product` - abstract base class (`ABC`, `get_fulfilment_info()` abstract) |
| `physical_product.py`     | `PhysicalProduct(Product, CanBeShipped)` - weight, shipping cost |
| `digital_product.py`      | `DigitalProduct(Product)` - download size                        |
| `subscription_product.py` | `SubscriptionProduct(Product)` - optional Section 8 task         |
| `can_be_shipped.py`       | `CanBeShipped` - interface-style ABC (`calculate_shipping_cost()`) |
| `product_types.py`        | Registry mapping `"physical"` / `"digital"` / `"subscription"` to classes |
| `inventory.py`            | `Inventory` - manages a list of products                        |
| `inventory_file.py`       | `InventoryFile` - JSON save/load, keeps product types            |
| `main.py`                 | Menu program                                                    |
| `demo.py`                 | Walk-through of Sections 1-4 (display, overriding, abstract error, shipping) |
| `test_lab7.py`            | Unit tests for the Section 7 checklist                          |
| `inventory.json`          | Test data with physical, digital and subscription products      |
| `UML.md`, `UML.png`, `UML.svg` | UML class diagram                                          |
| `reflection.md`           | Section 8 reflection                                            |
| `Dockerfile`              | Container for running the program and tests                     |

## Run locally

```
python main.py            # menu program
python demo.py            # Sections 1-4 walk-through
python -m unittest -v     # tests
```

## Run with Docker

```
docker build -t lab7-inventory .
docker run -it --rm lab7-inventory                        # menu program
docker run --rm lab7-inventory python -m unittest -v      # tests
docker run --rm lab7-inventory python demo.py             # walk-through
```

## Shipping rule

`calculate_shipping_cost() = 5.00 + 2.50 x weight (kg)`, e.g. 0.5 kg -> $6.25, 10 kg -> $30.00.
