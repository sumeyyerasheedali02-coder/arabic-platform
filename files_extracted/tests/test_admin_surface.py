"""Destructive maintenance operations must not be reachable over HTTP."""
import dataclasses

import pytest
from sqlalchemy import func, select

from ._app import main_module, models
import seed_database


@pytest.mark.parametrize("path", ["/api/admin/seed", "/api/admin/run-seed-now", "/api/run-seed"])
async def test_seeding_is_not_exposed_over_http(client, seed_spy, path):
    res = await client.get(path)
    assert res.status_code == 404
    assert seed_spy == []


async def test_seed_refuses_to_touch_a_database_that_has_content(register, client, content, db):
    student = await register()
    await client.post(f"/api/me/srs/add-unit/{content.unit_a}", headers=student.headers)

    with pytest.raises(seed_database.ContentExistsError):
        await seed_database.seed()

    cards = (await db.execute(select(func.count(models.SRSCard.id)))).scalar()
    units = (await db.execute(select(func.count(models.Unit.id)))).scalar()
    assert (cards, units) == (4, 2)


def test_replacing_content_from_the_command_line_needs_explicit_confirmation(seed_spy):
    with pytest.raises(SystemExit) as exit_info:
        seed_database._main(["--replace"])
    assert exit_info.value.code == 2
    assert seed_spy == []


async def test_startup_never_seeds_a_database_that_has_content(seed_spy):
    await main_module.on_startup()
    assert seed_spy == []


async def test_startup_bootstraps_only_an_empty_database_and_can_be_disabled(seed_spy, db, monkeypatch):
    for model in (models.Exercise, models.DialogueLine, models.Dialogue,
                  models.Vocabulary, models.Lesson, models.Unit):
        await db.execute(model.__table__.delete())
    await db.commit()

    disabled = dataclasses.replace(main_module.settings, seed_on_empty_db=False)
    monkeypatch.setattr(main_module, "settings", disabled)
    await main_module.on_startup()
    assert seed_spy == []

    enabled = dataclasses.replace(main_module.settings, seed_on_empty_db=True)
    monkeypatch.setattr(main_module, "settings", enabled)
    await main_module.on_startup()
    assert len(seed_spy) == 1 and seed_spy[0] == ((), {})
