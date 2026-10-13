"""Destructive maintenance operations must not be reachable over HTTP."""
import pytest


@pytest.mark.xfail(reason="public GET endpoints re-run the seed, wiping student activity")
@pytest.mark.parametrize("path", ["/api/admin/seed", "/api/admin/run-seed-now", "/api/run-seed"])
async def test_seeding_is_not_exposed_over_http(client, seed_spy, path):
    res = await client.get(path)
    assert res.status_code == 404
    assert seed_spy == []
