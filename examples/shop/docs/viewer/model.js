window.VOCKPIT_MODEL = {
  "diagrams": {
    "L0_context": {
      "title": "L0: Online Shop"
    },
    "L1_system": {
      "title": "L1: Online Shop"
    },
    "L2_orders": {
      "title": "L2: Orders"
    },
    "L2_storefront": {
      "title": "L2: Storefront"
    }
  },
  "edges": [
    {
      "data": "Browse and add to cart",
      "from": "customer",
      "to": "storefront"
    },
    {
      "data": "Cart",
      "from": "storefront",
      "to": "orders"
    },
    {
      "data": "Payment request",
      "from": "orders",
      "to": "payments"
    },
    {
      "data": "Card charge",
      "from": "payments",
      "to": "payment-provider"
    },
    {
      "data": "Payment result",
      "from": "payments",
      "to": "orders"
    },
    {
      "data": "Order event",
      "from": "orders",
      "to": "notifications"
    },
    {
      "data": "Order confirmation",
      "from": "notifications",
      "to": "customer"
    },
    {
      "data": "Shipping request",
      "from": "notifications",
      "to": "warehouse"
    },
    {
      "data": "Order request",
      "from": "order-controller",
      "to": "create-order"
    },
    {
      "data": "New order",
      "from": "create-order",
      "to": "order-repository"
    },
    {
      "data": "Payment result",
      "from": "order-controller",
      "to": "order-status"
    },
    {
      "data": "Status change",
      "from": "order-status",
      "to": "order-repository"
    },
    {
      "data": "Item to add",
      "from": "catalog-view",
      "to": "cart-store"
    },
    {
      "data": "Cart contents",
      "from": "cart-store",
      "to": "cart-view"
    },
    {
      "data": "Cart",
      "from": "cart-view",
      "to": "order-controller"
    }
  ],
  "generator": "vockpit 0.1.0",
  "nodes": {
    "cart-store": {
      "children": [],
      "code": [],
      "diagram": "L2_storefront",
      "id": "cart-store",
      "inputs": [],
      "kind": "box",
      "level": 2,
      "outputs": [],
      "parent": "storefront",
      "summary": "Keeps each customer's cart between visits.",
      "title": "Cart store"
    },
    "cart-view": {
      "children": [],
      "code": [],
      "diagram": "L2_storefront",
      "id": "cart-view",
      "inputs": [],
      "kind": "box",
      "level": 2,
      "outputs": [],
      "parent": "storefront",
      "summary": "Shows the cart and starts checkout.",
      "title": "Cart view"
    },
    "catalog-view": {
      "children": [],
      "code": [],
      "diagram": "L2_storefront",
      "id": "catalog-view",
      "inputs": [],
      "kind": "box",
      "level": 2,
      "outputs": [],
      "parent": "storefront",
      "summary": "Lists goods and shows one item in detail.",
      "title": "Catalogue view"
    },
    "create-order": {
      "children": [],
      "code": [],
      "diagram": "L2_orders",
      "id": "create-order",
      "inputs": [],
      "kind": "box",
      "level": 2,
      "outputs": [],
      "parent": "orders",
      "summary": "Validates a cart and turns it into an order.",
      "title": "Create order"
    },
    "customer": {
      "children": [],
      "diagram": "L0_context",
      "id": "customer",
      "inputs": [],
      "kind": "person",
      "level": null,
      "outputs": [],
      "parent": null,
      "summary": "Browses and buys goods.",
      "title": "Customer"
    },
    "notifications": {
      "children": [],
      "code": [],
      "diagram": "L1_system",
      "id": "notifications",
      "inputs": [
        "Order event"
      ],
      "kind": "box",
      "level": 1,
      "outputs": [],
      "parent": "shop",
      "summary": "Tells customers and the warehouse what happened.",
      "title": "Notifications"
    },
    "order-controller": {
      "children": [],
      "code": [],
      "diagram": "L2_orders",
      "id": "order-controller",
      "inputs": [],
      "kind": "box",
      "level": 2,
      "outputs": [],
      "parent": "orders",
      "summary": "Receives a checkout request and runs the steps.",
      "title": "Order controller"
    },
    "order-repository": {
      "children": [],
      "code": [],
      "diagram": "L2_orders",
      "id": "order-repository",
      "inputs": [],
      "kind": "box",
      "level": 2,
      "outputs": [],
      "parent": "orders",
      "summary": "Stores and retrieves orders.",
      "title": "Order repository"
    },
    "order-status": {
      "children": [],
      "code": [],
      "diagram": "L2_orders",
      "id": "order-status",
      "inputs": [],
      "kind": "box",
      "level": 2,
      "outputs": [],
      "parent": "orders",
      "summary": "Moves an order through new, paid and shipped.",
      "title": "Order status"
    },
    "orders": {
      "children": [
        "order-controller",
        "create-order",
        "order-repository",
        "order-status"
      ],
      "code": [],
      "diagram": "L2_orders",
      "id": "orders",
      "inputs": [
        "Cart"
      ],
      "kind": "box",
      "level": 1,
      "outputs": [
        "Order"
      ],
      "parent": "shop",
      "summary": "Takes orders and tracks them to delivery.",
      "title": "Orders"
    },
    "payment-provider": {
      "children": [],
      "diagram": "L0_context",
      "id": "payment-provider",
      "inputs": [],
      "kind": "external",
      "level": null,
      "outputs": [],
      "parent": null,
      "summary": "Takes card payments.",
      "title": "Payment Provider"
    },
    "payments": {
      "children": [],
      "code": [],
      "diagram": "L1_system",
      "id": "payments",
      "inputs": [
        "Order"
      ],
      "kind": "box",
      "level": 1,
      "outputs": [
        "Payment result"
      ],
      "parent": "shop",
      "summary": "Charges the customer for an order.",
      "title": "Payments"
    },
    "shop": {
      "children": [
        "storefront",
        "orders",
        "payments",
        "notifications"
      ],
      "diagram": "L1_system",
      "id": "shop",
      "inputs": [],
      "kind": "system",
      "level": 0,
      "outputs": [],
      "parent": null,
      "summary": "Lets customers browse goods, order them and pay online.",
      "title": "Online Shop"
    },
    "storefront": {
      "children": [
        "catalog-view",
        "cart-view",
        "cart-store"
      ],
      "code": [],
      "diagram": "L2_storefront",
      "id": "storefront",
      "inputs": [],
      "kind": "box",
      "level": 1,
      "outputs": [
        "Cart"
      ],
      "parent": "shop",
      "summary": "Shows the catalogue and the cart.",
      "title": "Storefront"
    },
    "warehouse": {
      "children": [],
      "diagram": "L0_context",
      "id": "warehouse",
      "inputs": [],
      "kind": "external",
      "level": null,
      "outputs": [],
      "parent": null,
      "summary": "Picks and ships orders.",
      "title": "Warehouse System"
    }
  },
  "system": "shop",
  "version": 1
};
