import pytest
from httpx import AsyncClient
from contextlib import nullcontext as does_not_raise

from src.core.exceptions import UserAlreadyExists
from src.models.users import Users


class TestAdminPanel:
    @pytest.mark.parametrize(
        "login, email, password, role, expected_status_code, exception",
        [
            ("newuser1", "newuser1@test.com", "secret3223FEF$%", "user", 201, does_not_raise()),
            ("admin1", "admin1@test.com", "secret3223FEF$%", "admin", 201, does_not_raise()),
            ("newuser2", "newuser2@test.com", "super1", "user", 422, does_not_raise()),
            ("newuser1", "newuser1@test.com", "secret3223FEF$%", "user", None, pytest.raises(UserAlreadyExists)),
        ]
    )
    async def test_create_user(self, admin_client: AsyncClient, login, email, password, role, expected_status_code, exception):
        with exception:
            new_user_data = {"login": login, "email": email, "password": password, "role": role}
            response = await admin_client.post("/admin/user", json=new_user_data)
            assert response.status_code == expected_status_code
            if response.status_code != 201:
                return

            data = response.json()
            assert data["login"] == new_user_data["login"]
            assert data["email"] == new_user_data["email"]

    async def test_get_users(self, admin_client: AsyncClient, create_user: Users):
        response = await admin_client.get("/admin/users")
        assert response.status_code == 200
        data = response.json()
        for user in data:
            if user["user_id"] != create_user.user_id:
                continue
            assert user["login"] == create_user.login
            return

        raise AssertionError("User not found")

    @pytest.mark.parametrize(
        "body, expected_status_code, exception",
        [
            ({"login": "1wddfsf", "password": "secret3223FEF$%wdfsd", "email": "fsdfsd@fwefw.com"}, 200, does_not_raise()),
            ({"password": "111"}, 422, does_not_raise()),
            ({"email": "fsdfsdewffwefw.com"}, 422, does_not_raise())
        ]
    )
    async def test_update_user(self, admin_client: AsyncClient, create_user: Users, body, expected_status_code, exception):
        old_user_login = create_user.login
        old_user_email = create_user.email
        with exception:
            response = await admin_client.patch(f"/admin/user/{create_user.user_id}", json=body)
            assert response.status_code == expected_status_code
            if response.status_code != 200:
                return

            data = response.json()
            assert data["login"] != old_user_login
            assert data["email"] != old_user_email

    async def test_delete_user(self, admin_client: AsyncClient, create_user: Users):
        response = await admin_client.delete(f"/admin/user/{create_user.user_id}")
        assert response.status_code == 204
