from pathlib import Path

from vockpit import registry


def test_load_good_fixture():
    root = Path(__file__).parent.parent / "fixtures" / "good"
    model, findings = registry.load(root)
    assert findings == []
    assert model is not None

    # System checks
    assert model.system.id == "shop"
    assert model.system.title == "Online Shop"
    assert model.system.summary == "Lets customers browse goods, order them and pay online."

    # Actors checks
    assert len(model.actors) == 3
    actor_ids = [a.id for a in model.actors]
    assert actor_ids == ["customer", "payment-provider", "warehouse"]
    assert model.actors[0].kind == "person"
    assert model.actors[1].kind == "external"

    # Boxes checks
    # L1: storefront, orders, payments, notifications
    # L2: storefront -> catalog-view, cart-view, cart-store
    # L2: orders -> order-controller, create-order, order-repository, order-status
    assert len(model.boxes) == 4 + 3 + 4

    # Check L1 boxes
    storefront = next(b for b in model.boxes if b.id == "storefront")
    assert storefront.level == 1
    assert storefront.parent == "shop"
    assert storefront.children == ["catalog-view", "cart-view", "cart-store"]
    assert storefront.source == "model/system.yaml"
    assert storefront.outputs == ["Cart"]

    orders = next(b for b in model.boxes if b.id == "orders")
    assert orders.level == 1
    assert orders.parent == "shop"
    assert orders.children == [
        "order-controller",
        "create-order",
        "order-repository",
        "order-status",
    ]

    payments = next(b for b in model.boxes if b.id == "payments")
    assert payments.level == 1
    assert payments.children == []

    # Check L2 boxes
    create_order = next(b for b in model.boxes if b.id == "create-order")
    assert create_order.level == 2
    assert create_order.parent == "orders"
    assert create_order.children == []
    assert create_order.source == "model/boxes/orders.yaml"

    # Edges checks
    # 8 from system.yaml + 3 from storefront.yaml + 4 from orders.yaml = 15 edges
    assert len(model.edges) == 15
    first_edge = model.edges[0]
    assert first_edge.from_id == "customer"
    assert first_edge.to_id == "storefront"
    assert first_edge.data == "Browse and add to cart"
    assert first_edge.source == "model/system.yaml"


def test_load_missing_system_yaml(tmp_path):
    model, findings = registry.load(tmp_path)
    assert model is None
    assert len(findings) == 1
    assert findings[0].rule == "C01"
    assert findings[0].severity == "ERROR"
    assert "model/system.yaml" in findings[0].location
