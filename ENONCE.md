# Exercice : consommation de fichiers CSV


| Fichier               | Contenu                                   | Lignes |
|-----------------------|-------------------------------------------|--------|
| `suppliers.csv`       | les fournisseurs                          | 52     |
| `purchase_orders.csv` | les commandes passées aux fournisseurs    | 62     |
| `stock_moves.csv`     | les entrées et sorties de stock           | 182    |

Les exercices vont **du plus simple au plus compliqué**. Fais-les dans l'ordre.

---

## Rappels

- Tous les fichiers sont séparés par des **points-virgules** : `delimiter=";"`.
- Ouvre les fichiers en `encoding="utf-8"` (il y a des accents).
- **Tout ce qui sort d'un CSV est du texte.** Pense à convertir avec `int()` et `float()`.
- Garde la même structure que pour les produits :
  - la classe du modèle dans `models/`,
  - le manager dans `managers/`,
  - le menu dans `main.py` (à la racine).
- On lance toujours le programme depuis la racine : `python main.py`.

---

## Niveau 1 : les fournisseurs (`suppliers.csv`)

C'est le plus simple : toutes les colonnes sont du texte, il n'y a **aucune conversion** à faire.

```
reference;name;email;phone;city
SUP-001;InfoExpress SRL;commandes@infoexpress.be;+32 67 56 69 64;Nivelles
```

1. Crée la classe `Supplier` dans `models/supplier.py`, avec les 5 attributs et une méthode `__str__`.
2. Crée `SupplierManager` dans `managers/supplier_manager.py`, avec les méthodes suivantes :
   - `load_suppliers()` : lit le CSV et remplit la liste `self.suppliers` ;
   - `display_suppliers()` : affiche tous les fournisseurs ;
   - `find_by_reference(reference)` : renvoie **un** fournisseur, ou `None` ;
   - `find_by_city(city)` : renvoie la **liste** des fournisseurs d'une ville ;
   - `find_all_cities()` : renvoie la liste des villes, **sans doublon** et triée.

**Pour vérifier :** il y a 52 fournisseurs et 14 villes différentes. À Ottignies, tu dois trouver 7 fournisseurs.

---

## Niveau 2 : les commandes (`purchase_orders.csv`)

Ce niveau ajoute des **conversions** et une **valeur vide**.

```
reference;supplier_reference;product_reference;quantity;unit_cost;state;order_date;receipt_date
PO-0001;SUP-026;TR-001;45;3.09;received;2026-06-03;2026-06-08
PO-0005;SUP-036;PR-LAS;6;91.57;confirmed;2026-06-08;
```

Points d'attention :
- `quantity` est un `int` et `unit_cost` un `float` ;
- `state` peut valoir `draft`, `confirmed`, `received` ou `cancelled` ;
- `receipt_date` est **vide** quand la commande n'est pas encore reçue (regarde la fin de la ligne `PO-0005`). Dans ce cas, stocke `None` au lieu d'une chaîne vide.

1. Crée la classe `PurchaseOrder` et ajoute-lui une méthode `get_total()` qui renvoie `quantity * unit_cost`.
2. Crée `PurchaseOrderManager` avec les méthodes suivantes :
   - `load_purchase_orders()` ;
   - `display_purchase_orders()` ;
   - `find_by_reference(reference)` ;
   - `find_by_state(state)` : par exemple, toutes les commandes `received` ;
   - `find_by_supplier(supplier_reference)` : toutes les commandes d'un fournisseur.
3. **Un peu plus dur :** écris `find_by_order_date(start_date, end_date)`, qui renvoie les commandes passées entre deux dates.
   > Les dates sont au format `AAAA-MM-JJ`. Avec ce format, comparer deux chaînes donne le bon résultat : `"2026-06-03" < "2026-07-01"` vaut `True`.
   > Si tu veux aller plus loin, utilise plutôt `datetime.strptime(date_text, "%Y-%m-%d")`.

 **Pour vérifier :**
- états : 45 `received`, 6 `confirmed`, 5 `draft` et 6 `cancelled` ;
- le total de `PO-0001` vaut 139,05 €. Utilise `round(..., 2)`, sinon tu obtiendras `139.04999999999998`.

---

## Niveau 3 : les mouvements de stock (`stock_moves.csv`)

```
date;product_reference;move_type;quantity;origin
2026-06-01;ST-001;receipt;24;Inventaire initial
2026-06-03;CH-001;delivery;3;Service interne
```

- `move_type` vaut `receipt` (une **entrée** en stock) ou `delivery` (une **sortie**).
- `quantity` est **toujours positive**. C'est le type de mouvement qui dit si on ajoute ou si on retire.
- `origin` indique d'où vient le mouvement : `Inventaire initial`, `Commande web`, `Service interne`, ou une référence de commande comme `PO-0001`.

1. Crée la classe `StockMove`.
2. Crée `StockMoveManager` avec les méthodes suivantes :
   - `load_stock_moves()` ;
   - `display_stock_moves()` ;
   - `find_by_product(product_reference)` : l'historique complet d'un produit ;
   - `find_by_move_type(move_type)` : toutes les entrées, ou toutes les sorties ;
   - `find_by_date_range(start_date, end_date)`.

**Pour vérifier :** il y a 182 mouvements au total, dont 71 `receipt` et 111 `delivery`.

---

## Niveau 4 : croiser les fichiers (le plus compliqué)

Jusqu'ici, chaque manager travaillait **seul**. Maintenant, on relie les fichiers entre eux grâce aux références.

```
suppliers.reference  ←──  purchase_orders.supplier_reference
products.reference   ←──  purchase_orders.product_reference
products.reference   ←──  stock_moves.product_reference
```

> Pour que deux managers puissent se parler, crée-les tous dans `main.py`, puis passe-les en paramètre aux fonctions ou aux méthodes qui en ont besoin.

### 4.1 Afficher une commande lisible

Une commande affichée seule donne `PO-0001 | SUP-026 | TR-001 | ...`, ce qui n'est pas très parlant.
Écris une fonction qui affiche la commande avec le **nom** du fournisseur et le **nom** du produit :

```
PO-0001 | <nom du fournisseur> | Sacs poubelle x50 | 45 x 3.09 € = 139.05 € | received
```

### 4.2 Calculer le stock actuel d'un produit

Le stock d'un produit vaut : **somme des `receipt` − somme des `delivery`**.

Écris `get_current_stock(product_reference)` dans `StockMoveManager`.

**Pour vérifier :** `KB-001` doit avoir un stock de **20**.

### 4.3 Produits sous le stock minimum

Chaque produit a une `minimum_quantity` (dans `products.csv`).
Affiche tous les produits dont le stock actuel est **inférieur** à leur quantité minimum : ce sont ceux qu'il faut recommander.

**Pour vérifier :** tu dois trouver 29 produits (entre autres `MS-001`, `SC-027` et `KB-WL`).

### 4.4 Total acheté par fournisseur

Pour un fournisseur donné, calcule le montant total de ses commandes **reçues** (`received`).
Ensuite, calcule le total de **toutes** les commandes reçues, tous fournisseurs confondus.

**Pour vérifier :** le total de toutes les commandes reçues vaut **17 219,78 €**.

---

## Niveau 5 : le menu principal

Regroupe tout dans `main.py`, avec un menu principal qui ouvre un **sous-menu** par fichier :

```
===== MENU PRINCIPAL =====
1 - Produits
2 - Fournisseurs
3 - Commandes
4 - Mouvements de stock
5 - Rapports (niveau 4)
0 - Quitter
```

Chaque sous-menu reprend les actions de son manager et propose une option `0 - Retour`.

---

## Bonus

- Liste les fournisseurs qui n'ont **aucune** commande (il y en a 22).
- Trouve les fournisseurs qui ont le **plus** de commandes.
- gère l'ajout et la suppression
