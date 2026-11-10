from vockpit.findings import Finding, format_findings


def test_finding_formatting():
    f = Finding(
        rule="C02",
        severity="ERROR",
        location="model/boxes/orders.yaml",
        message="duplicate id 'create-order' (also in model/system.yaml)",
    )
    assert str(f) == "C02 ERROR model/boxes/orders.yaml: duplicate id 'create-order' (also in model/system.yaml)"


def test_findings_sorting():
    f1 = Finding(rule="C02", severity="ERROR", location="model/boxes/b.yaml", message="msg 1")
    f2 = Finding(rule="C01", severity="ERROR", location="model/system.yaml", message="msg 2")
    f3 = Finding(rule="C02", severity="ERROR", location="model/boxes/a.yaml", message="msg 3")
    sorted_findings = sorted([f1, f2, f3])
    assert sorted_findings == [f2, f3, f1]
    formatted = format_findings([f1, f2, f3])
    lines = formatted.splitlines()
    assert lines[0].startswith("C01")
    assert lines[1].startswith("C02 ERROR model/boxes/a.yaml")
    assert lines[2].startswith("C02 ERROR model/boxes/b.yaml")
