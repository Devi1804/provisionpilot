from agent.tools import render_vagrantfile, render_inventory

SPEC = {
    "vms": [
        {"name": "web1", "role": "web"},
        {"name": "db1", "role": "db"},
    ],
    "memory_mb": 2048,
    "cpus": 2,
}


def test_render_vagrantfile_includes_all_vms():
    out = render_vagrantfile(SPEC)["rendered"]
    assert "web1" in out
    assert "db1" in out
    assert 'qe.memory = "2048"' in out


def test_render_inventory_groups_by_role():
    out = render_inventory(SPEC)["rendered"]
    assert "[web]" in out
    assert "[db]" in out
    assert "web1" in out