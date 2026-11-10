from pathlib import Path
import pytest
from vockpit.diagrams import Diagram, DiagramNode, DiagramEdge
from vockpit import d2


def test_d2_render_deterministic():
    diag = Diagram(
        name="L2_orders",
        title="L2: Orders",
        nodes=[
            DiagramNode(
                id="create-order",
                title="Create order",
                summary="Validates a cart and stores the order.",
                role="inner",
                link="#/create-order",
            ),
            DiagramNode(
                id="customer",
                title="Customer",
                summary="Buys goods.",
                role="person",
                link="",
            ),
        ],
        edges=[
            DiagramEdge(
                from_id="order-controller",
                to_id="create-order",
                label="OrderRequest",
            )
        ],
    )

    out1 = d2.render(diag)
    out2 = d2.render(diag)
    assert out1 == out2
    assert "classes: {" in out1
    assert 'n_create_order: "Create order" {' in out1
    assert '  class: inner' in out1
    assert '  link: "#/create-order"' in out1
    assert '  tooltip: "Validates a cart and stores the order."' in out1
    assert 'n_customer: "Customer" {' in out1
    assert '  shape: person' in out1
    assert 'n_order_controller -> n_create_order: "OrderRequest"' in out1


def test_d2_escaping():
    diag = Diagram(
        name="L1_escape",
        title="L1: Test Escaping",
        nodes=[
            DiagramNode(
                id="node-1",
                title='Box "One" & Two',
                summary="Line 1\nLine 2 with \\backslash",
                role="inner",
                link="#/node-1",
            )
        ],
        edges=[
            DiagramEdge(
                from_id="node-1",
                to_id="node-1",
                label='Sends "data" with \\slash and\nnewline',
            )
        ],
    )
    rendered = d2.render(diag)
    assert 'n_node_1: "Box \\"One\\" & Two" {' in rendered
    assert 'tooltip: "Line 1 Line 2 with \\\\backslash"' in rendered
    assert 'n_node_1 -> n_node_1: "Sends \\"data\\" with \\\\slash and newline"' in rendered


def test_d2_svg_rendering(tmp_path):
    d2_bin = d2.find_d2_executable()
    if not d2_bin:
        pytest.skip("d2 executable not found")

    diag = Diagram(
        name="L2_orders",
        title="L2: Orders",
        nodes=[
            DiagramNode(
                id="create-order",
                title="Create order",
                summary="Validates a cart and stores the order.",
                role="inner",
                link="#/create-order",
            )
        ],
        edges=[],
    )
    d2_text = d2.render(diag)
    d2_file = tmp_path / "L2_orders.d2"
    svg_file = tmp_path / "L2_orders.svg"
    d2_file.write_text(d2_text, encoding="utf-8")

    d2.to_svg(d2_file, svg_file, d2_bin=d2_bin)
    assert svg_file.is_file()
    svg_content = svg_file.read_text(encoding="utf-8")
    assert "#/create-order" in svg_content
