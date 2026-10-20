# Exercise: reading CSV files


| File                  | Content                                   | Lines |
|-----------------------|-------------------------------------------|-------|
| `suppliers.csv`       | the suppliers                             | 52    |
| `purchase_orders.csv` | the orders sent to the suppliers          | 62    |
| `stock_moves.csv`     | the stock receipts and deliveries         | 182   |

The exercises go **from the easiest to the hardest**. Do them in order.

---

## Reminders

- All files are separated by **semicolons**: `delimiter=";"`.
- Open the files with `encoding="utf-8"` (they contain accented characters).
- **Everything read from a CSV is a string.** Remember to convert with `int()` and `float()`.
- Keep the same structure as for the products:
  - the model class in `models/`,
  - the manager in `managers/`,
  - the menu in `main.py` (at the root).
- Always run the program from the root: `python main.py`.

---

## Level 1: suppliers (`suppliers.csv`)

This is the easiest one: every column is text, so **no conversion** is needed.

```
reference;name;email;phone;city
SUP-001;InfoExpress SRL;commandes@infoexpress.be;+32 67 56 69 64;Nivelles
```

1. Create the `Supplier` class in `models/supplier.py`, with the 5 attributes and a `__str__` method.
2. Create `SupplierManager` in `managers/supplier_manager.py`, with the following methods:
   - `load_suppliers()`: reads the CSV and fills the `self.suppliers` list;
   - `display_suppliers()`: displays every supplier;
   - `find_by_reference(reference)`: returns **one** supplier, or `None`;
   - `find_by_city(city)`: returns the **list** of suppliers in a city;
   - `find_all_cities()`: returns the list of cities, **without duplicates** and sorted.

**To check:** there are 52 suppliers and 14 different cities. In Ottignies, you should find 7 suppliers.

---

## Level 2: purchase orders (`purchase_orders.csv`)

This level adds **conversions** and an **empty value**.

```
reference;supplier_reference;product_reference;quantity;unit_cost;state;order_date;receipt_date
PO-0001;SUP-026;TR-001;45;3.09;received;2026-06-03;2026-06-08
PO-0005;SUP-036;PR-LAS;6;91.57;confirmed;2026-06-08;
```

Watch out:
- `quantity` is an `int` and `unit_cost` is a `float`;
- `state` can be `draft`, `confirmed`, `received` or `cancelled`;
- `receipt_date` is **empty** when the order has not been received yet (look at the end of the `PO-0005` line). In that case, store `None` instead of an empty string.

1. Create the `PurchaseOrder` class and give it a `get_total()` method that returns `quantity * unit_cost`.
2. Create `PurchaseOrderManager` with the following methods:
   - `load_purchase_orders()`;
   - `display_purchase_orders()`;
   - `find_by_reference(reference)`;
   - `find_by_state(state)`: for example, every `received` order;
   - `find_by_supplier(supplier_reference)`: every order of one supplier.
3. **A bit harder:** write `find_by_order_date(start_date, end_date)`, which returns the orders placed between two dates.
   > Dates use the `YYYY-MM-DD` format. With this format, comparing two strings gives the right result: `"2026-06-03" < "2026-07-01"` is `True`.
   > To go further, use `datetime.strptime(date_text, "%Y-%m-%d")` instead.

**To check:**
- states: 45 `received`, 6 `confirmed`, 5 `draft` and 6 `cancelled`;
- the total of `PO-0001` is €139.05. Use `round(..., 2)`, otherwise you will get `139.04999999999998`.

---

## Level 3: stock moves (`stock_moves.csv`)

```
date;product_reference;move_type;quantity;origin
2026-06-01;ST-001;receipt;24;Inventaire initial
2026-06-03;CH-001;delivery;3;Service interne
```

- `move_type` is either `receipt` (stock **coming in**) or `delivery` (stock **going out**).
- `quantity` is **always positive**. The move type tells you whether to add or subtract.
- `origin` says where the move comes from: `Inventaire initial` (initial inventory), `Commande web` (web order), `Service interne` (internal department), or an order reference such as `PO-0001`.

1. Create the `StockMove` class.
2. Create `StockMoveManager` with the following methods:
   - `load_stock_moves()`;
   - `display_stock_moves()`;
   - `find_by_product(product_reference)`: the full history of one product;
   - `find_by_move_type(move_type)`: every receipt, or every delivery;
   - `find_by_date_range(start_date, end_date)`.

**To check:** there are 182 moves in total: 71 `receipt` and 111 `delivery`.

---

## Level 4: linking the files together (the hardest)

Until now, each manager worked **on its own**. Now we link the files to each other through their references.

```
suppliers.reference  ←──  purchase_orders.supplier_reference
products.reference   ←──  purchase_orders.product_reference
products.reference   ←──  stock_moves.product_reference
```

> For two managers to talk to each other, create all of them in `main.py`, then pass them as parameters to the functions or methods that need them.

### 4.1 Display a readable order

An order displayed on its own gives `PO-0001 | SUP-026 | TR-001 | ...`, which is not very meaningful.
Write a function that displays the order with the supplier's **name** and the product's **name**:

```
PO-0001 | <supplier name> | Sacs poubelle x50 | 45 x 3.09 € = 139.05 € | received
```

### 4.2 Compute the current stock of a product

The stock of a product is: **sum of the `receipt` quantities − sum of the `delivery` quantities**.

Write `get_current_stock(product_reference)` in `StockMoveManager`.

**To check:** `KB-001` should have a stock of **20**.

### 4.3 Products below the minimum stock

Each product has a `minimum_quantity` (in `products.csv`).
Display every product whose current stock is **lower** than its minimum quantity: these are the ones to reorder.

**To check:** you should find 29 products (including `MS-001`, `SC-027` and `KB-WL`).

### 4.4 Total purchased per supplier

For a given supplier, compute the total amount of its **received** orders (`received`).
Then compute the total of **all** received orders, for all suppliers combined.

**To check:** the total of all received orders is **€17,219.78**.

---

## Level 5: the main menu

Bring everything together in `main.py`, with a main menu that opens one **submenu** per file:

```
===== MAIN MENU =====
1 - Products
2 - Suppliers
3 - Purchase orders
4 - Stock moves
5 - Reports (level 4)
0 - Quit
```

Each submenu offers the actions of its manager and a `0 - Back` option.

---

## Bonus

- List the suppliers that have **no** orders (there are 22).
- Find the suppliers with the **most** orders.
- Handle adding and deleting
