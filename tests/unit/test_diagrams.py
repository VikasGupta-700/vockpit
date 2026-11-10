from pathlib import Path
from vockpit import registry, diagrams

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"


def test_build_diagrams_shop():
    root = FIXTURES_DIR / "good"
    model, _ = registry.load(root)
    assert model is not None

    diag_list = diagrams.build(model)
    diag_map = {d.name: d for d in diag_list}

    # Diagrams: L0_context, L1_system, L2_storefront, L2_orders.
    assert list(diag_map.keys()) == ["L0_context", "L1_system", "L2_storefront", "L2_orders"]

    # L0_context has 4 nodes and 4 edges: customer -> shop, shop -> customer, shop -> payment-provider, shop -> warehouse.
    l0 = diag_map["L0_context"]
    assert l0.title == "L0: Online Shop"
    assert len(l0.nodes) == 4
    assert [n.id for n in l0.nodes] == ["shop", "customer", "payment-provider", "warehouse"]
    assert len(l0.edges) == 4
    l0_edge_pairs = [(e.from_id, e.to_id, e.label) for e in l0.edges]
    assert l0_edge_pairs == [
        ("customer", "shop", "Browse and add to cart"),
        ("shop", "customer", "Order confirmation"),
        ("shop", "payment-provider", "Card charge"),
        ("shop", "warehouse", "Shipping request"),
    ]

    # L1_system has 4 inner nodes and 3 actor nodes.
    l1 = diag_map["L1_system"]
    assert l1.title == "L1: Online Shop"
    inner_l1 = [n for n in l1.nodes if n.role == "inner"]
    actor_l1 = [n for n in l1.nodes if n.role in ("person", "external")]
    assert len(inner_l1) == 4
    assert [n.id for n in inner_l1] == ["storefront", "orders", "payments", "notifications"]
    assert len(actor_l1) == 3
    assert [n.id for n in actor_l1] == ["customer", "payment-provider", "warehouse"]

    # L2_storefront has 3 inner nodes and the neighbour orders, reached by the edge cart-view -> orders.
    l2_sf = diag_map["L2_storefront"]
    assert l2_sf.title == "L2: Storefront"
    inner_sf = [n for n in l2_sf.nodes if n.role == "inner"]
    neigh_sf = [n for n in l2_sf.nodes if n.role == "neighbour"]
    assert len(inner_sf) == 3
    assert [n.id for n in inner_sf] == ["catalog-view", "cart-view", "cart-store"]
    assert len(neigh_sf) == 1
    assert neigh_sf[0].id == "orders"
    sf_edge_pairs = [(e.from_id, e.to_id, e.label) for e in l2_sf.edges]
    assert ("cart-view", "orders", "Cart") in sf_edge_pairs

    # L2_orders has 4 inner nodes and the neighbour storefront, from the edge storefront -> orders.
    # Edges declared in system.yaml between orders and payments or notifications do not appear,
    # because their orders end maps to the focus itself, which is not an inner node.
    l2_ord = diag_map["L2_orders"]
    assert l2_ord.title == "L2: Orders"
    inner_ord = [n for n in l2_ord.nodes if n.role == "inner"]
    neigh_ord = [n for n in l2_ord.nodes if n.role == "neighbour"]
    assert len(inner_ord) == 4
    assert [n.id for n in inner_ord] == ["order-controller", "create-order", "order-repository", "order-status"]
    assert len(neigh_ord) == 1
    assert neigh_ord[0].id == "storefront"
    ord_edge_pairs = [(e.from_id, e.to_id, e.label) for e in l2_ord.edges]
    assert ord_edge_pairs == [
        ("create-order", "order-repository", "New order"),
        ("order-controller", "create-order", "Order request"),
        ("order-controller", "order-status", "Payment result"),
        ("order-status", "order-repository", "Status change"),
        ("storefront", "order-controller", "Cart"),
    ]
