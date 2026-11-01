# Lab 7 - Reflection (Section 8, optional)

## Adding `SubscriptionProduct`

`SubscriptionProduct` (in `subscription_product.py`) inherits from `Product`, reuses its
constructor with `super()`, adds a `billing_months` attribute, overrides `display_information()`
(calling the parent first) and implements the abstract `get_fulfilment_info()`. It does not
implement `CanBeShipped`, because nothing is shipped.

## How well does the design support a new product type?

Fairly well. To add the new type I had to:

| File                       | Changed? | Why                                                       |
|----------------------------|----------|-----------------------------------------------------------|
| `product.py`               | No       | Closed for modification - only extended                   |
| `physical_product.py`, `digital_product.py` | No | Each type is independent                    |
| `inventory.py`             | No       | It only calls `Product` methods, never checks the type    |
| `inventory_file.py`        | No       | Each product writes its own `to_dict()`; loading looks the class up in the registry |
| `main.py`                  | No       | The "choose type" menu is built from the registry         |
| `subscription_product.py`  | **New**  | The new class                                             |
| `product_types.py`         | **1 line** | Register the new type id, label, class and extra prompt |

## Which parts needed to change, and why?

In a straightforward first version, three places would have needed editing for every new type:

1. **`InventoryFile.save()`** - an `if isinstance(product, PhysicalProduct): ... elif ...` chain to
   decide which extra attributes to write.
2. **`InventoryFile.load()`** - an `if item["type"] == "physical": ... elif ...` chain to decide
   which class to create.
3. **`main.py` `menu_add()`** - another `if/elif` chain for the type menu and the extra prompt.

Each `if/elif` chain breaks the Open-Closed Principle: the code has to be *modified* (not just
extended) every time a new type appears, and it is easy to forget one of the three places.

## How the design was enhanced (not an inheritance solution)

- **Each product serialises itself.** `Product.to_dict()` returns the common fields and every
  subclass overrides it (calling `super().to_dict()`) to add its `"type"` and extra attribute.
  A matching `from_dict()` class method rebuilds the object. `InventoryFile.save()` therefore just
  calls `product.to_dict()` - no type checks.
- **A registry / factory instead of `if/elif`.** `product_types.py` holds one dictionary,
  `PRODUCT_TYPES`, that maps a type identifier (`"physical"`, `"digital"`, `"subscription"`) to its
  class, menu label and extra-attribute prompt. `InventoryFile.load()` looks up the class from the
  saved `"type"` and calls `from_dict()`; `main.py` builds the "Product Type" menu from the same
  dictionary. This is a *composition / lookup-table* approach rather than inheritance.

The remaining cost is one registry line per new type. That could be removed too - e.g. each
subclass registers itself automatically (a decorator or `__init_subclass__`), or classes are
discovered from a plug-in folder - but a single explicit registry is easier to read and test, so
it was kept.

One trade-off: putting `to_dict()` on the products means the product classes know their saved
format, which slightly blurs SRP with `InventoryFile`. The alternative (all JSON knowledge inside
`InventoryFile`) keeps SRP purer but forces `InventoryFile` to change for every new type. For this
system, keeping product types open for extension was judged the more useful property.
