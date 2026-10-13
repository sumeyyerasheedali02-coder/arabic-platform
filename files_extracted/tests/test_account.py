from datetime import timedelta

import pytest

from app.routers import account
from app.security import create_access_token

from . import _app  # noqa: F401 - identify the temporary test database before app imports


@pytest.fixture(autouse=True)
def clear_limits():
    account._requests.clear()


@pytest.mark.parametrize("role", ["student", "teacher", "admin"])
async def test_self_service_preserves_role_and_identifiers(client, register, teacher, admin, role):
    person = await {"student": register, "teacher": teacher, "admin": admin}[role]()
    before = (await client.get('/api/account/me', headers=person.headers)).json()
    saved = await client.patch('/api/account/me', headers=person.headers,
                               json={"name": "  اسم جديد  ", "role": "admin", "student_number": "999"})
    assert saved.status_code == 200
    assert saved.json()['name'] == 'اسم جديد'
    after = (await client.get('/api/account/me', headers=person.headers)).json()
    assert after == {**before, 'name': 'اسم جديد'}
    assert (await client.patch('/api/account/me', headers=person.headers,
                               json={'name': '   '})).status_code == 422


async def test_password_requires_current_password_and_revokes_sessions(client, register, login):
    person = await register(password='old-password')
    assert (await client.post('/api/account/password', headers=person.headers,
                             json={'current_password': 'wrong', 'password': 'new-password'})).status_code == 400
    saved = await client.post('/api/account/password', headers=person.headers,
                              json={'current_password': 'old-password', 'password': 'new-password'})
    assert saved.status_code == 200
    assert (await client.get('/api/auth/me', headers=person.headers)).status_code == 401
    headers = {'Authorization': f"Bearer {saved.json()['access_token']}"}
    assert (await client.get('/api/auth/me', headers=headers)).status_code == 200
    profile = (await client.get('/api/account/me', headers=headers)).json()
    assert (await login(profile['email'], 'old-password')).status_code == 401
    assert (await login(profile['email'], 'new-password')).status_code == 200


async def test_reset_links_expire_are_single_use_and_never_authenticate(client, register, monkeypatch):
    person = await register()
    deliveries = []
    monkeypatch.setattr(account, 'mail_ready', lambda: True)
    monkeypatch.setattr(account, 'send_reset_email', lambda address, token: deliveries.append(token))
    email = (await client.get('/api/account/me', headers=person.headers)).json()['email']
    response = await client.post('/api/account/forgot-password', json={'email': email})
    unknown = await client.post('/api/account/forgot-password', json={'email': 'unknown@example.com'})
    assert response.json() == unknown.json()
    assert len(deliveries) == 1
    token = deliveries[0]
    assert (await client.get('/api/auth/me', headers={'Authorization': f'Bearer {token}'})).status_code == 401
    assert (await client.post('/api/account/reset-password', json={
        'token': person.body['access_token'], 'password': 'new-password'})).status_code == 400
    expired = create_access_token({'sub': str(person.id), 'ver': 0, 'purpose': 'password-reset'},
                                  timedelta(seconds=-1))
    assert (await client.post('/api/account/reset-password', json={
        'token': expired, 'password': 'new-password'})).status_code == 400
    assert (await client.post('/api/account/reset-password', json={
        'token': token, 'password': 'new-password'})).status_code == 200
    assert (await client.post('/api/account/reset-password', json={
        'token': token, 'password': 'another-password'})).status_code == 400
    assert (await client.get('/api/auth/me', headers=person.headers)).status_code == 401


async def test_recovery_disabled_and_throttled(client, monkeypatch):
    monkeypatch.setattr(account, 'mail_ready', lambda: False)
    assert (await client.post('/api/account/forgot-password', json={'email': 'a@example.com'})).status_code == 503
    monkeypatch.setattr(account, 'mail_ready', lambda: True)
    for _ in range(3):
        assert (await client.post('/api/account/forgot-password', json={'email': 'a@example.com'})).status_code == 200
    assert (await client.post('/api/account/forgot-password', json={'email': 'a@example.com'})).status_code == 429


async def test_password_length_and_auth_required(client, register):
    assert (await client.get('/api/account/me')).status_code == 401
    person = await register()
    for password in ['short', 'ع' * 40]:
        assert (await client.post('/api/account/password', headers=person.headers,
                                 json={'current_password': 'secret123', 'password': password})).status_code == 422
