"""
Tests for the Django admin modifications.
"""

from typing import Any, cast

from django.test import Client, TestCase
from django.urls import reverse

from core.models import User, UserManager


class AdminSiteTests(TestCase):
    """Tests for Django admin."""

    client: Client
    admin_user: User = cast(User, User())
    user: User = cast(User, User())

    @staticmethod
    def user_manager() -> UserManager:
        """Return the concrete user manager for type checking."""
        return cast(UserManager, User.objects)

    def setUp(self) -> None:
        """Create user and client."""
        self.client = Client()
        self.admin_user = self.user_manager().create_superuser(
            email="admin@example.com", password="testpass123"
        )
        self.client.force_login(self.admin_user)
        self.user = self.user_manager().create_user(
            email="user@example.com",
            password="testpass123",
            name="Test User",
        )
        return super().setUp()

    def test_users_list(self):
        """Test that users are listed on page."""
        url = reverse("admin:core_user_changelist")
        res = self.client.get(url)
        typed_user = cast(Any, self.user)

        self.assertContains(res, typed_user.name)
        self.assertContains(res, typed_user.email)

    def test_edit_page(self):
        """Test the edit user page works."""
        typed_user = cast(Any, self.user)
        url = reverse("admin:core_user_change", args=[typed_user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test the create user page works."""
        url = reverse("admin:core_user_add")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
