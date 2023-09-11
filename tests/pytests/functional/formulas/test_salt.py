"""
Tests using salt formula
"""

import pytest


@pytest.fixture(scope="module")
def _formula(saltstack_formula):
    with saltstack_formula(name="salt-formula", tag="1.12.0") as formula:
        yield formula


@pytest.fixture(scope="module")
def modules(loaders, _formula):
    loaders.opts["file_roots"]["base"].append(
        str(_formula.state_tree_path / f"{_formula.name}-{_formula.tag}")
    )
    return loaders.modules


@pytest.mark.skip_on_windows
@pytest.mark.destructive_test
# These installation issues need to be resolved in the Salt formula, and then
# we can update the tag in here and remove the skips
@pytest.mark.skipif(
    'grains["osfullname"] in ("AlmaLinux", "Amazon Linux")',
    reason="No salt packages available for this distrubition",
)
@pytest.mark.skipif(
    'grains["os"] == "CentOS"',
    reason="No salt packages available for this distrubition",
)
@pytest.mark.skipif(
    'grains["os_family"] == "Arch"',
    reason="Outdated archlinux-keyring package will cause failed package installs",
)
def test_salt_formula(modules):
    # Master Formula
    ret = modules.state.sls("salt.master")
    assert not ret.errors
    # asserting not ret.failed will cause a False positive if ret.failed is None
    assert ret.failed is not True
    for staterun in ret:
        assert staterun.result

    # Minion Formula
    ret = modules.state.sls("salt.minion")
    assert not ret.errors
    # asserting not ret.failed will cause a False positive if ret.failed is None
    assert ret.failed is not True
    for staterun in ret:
        assert staterun.result
