"""
Tests for models.
"""

from decimal import Decimal
from typing import Any, cast
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase

from core import models
from core.models import Ingredient, Recipe, Tag, User, UserManager


def create_user(email="user@example.com", password="testpaww123"):
    """Create and return a new user."""
    return get_user_model().objects.create_user(email, password)


class ModelTest(TestCase):
    """Test models."""

    @staticmethod
    def user_manager() -> UserManager:
        """Return the concrete user manager for type checking."""
        return cast(UserManager, User.objects)

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = "test@example.com"
        password = "testpass123"
        user = self.user_manager().create_user(
            email=email,
            password=password,
        )
        typed_user = cast(Any, user)

        self.assertEquals(typed_user.email, email)
        self.assertTrue(typed_user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@Example.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.COM", "TEST3@example.com"],
            ["test4@example.COM", "test4@example.com"],
        ]

        for email, expected in sample_emails:
            user = self.user_manager().create_user(email, "sample123")
            typed_user = cast(Any, user)
            self.assertEquals(typed_user.email, expected)

    def test_creating_superuser(self):
        """Test creating a superuser"""
        user = self.user_manager().create_superuser(
            "test@example.com",
            "test123",
        )
        typed_user = cast(Any, user)

        self.assertTrue(typed_user.is_superuser)
        self.assertTrue(typed_user.is_staff)

    def test_create_recipe(self):
        """Test creating a recipe is successful."""
        user = self.user_manager().create_user(
            "test@example.com",
            "testpass123",
        )

        recipe = Recipe.objects.create(
            user=user,
            title="Sameple recipe name",
            time_minutes=5,
            price=Decimal("5.50"),
            description="Sample recipe description.",
        )

        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        """Test creating a tag is successful."""
        user = create_user()
        tag = Tag.objects.create(user=user, name="Tag1")

        self.assertEqual(str(tag), tag.name)

    def test_create_ingredient(self):
        """Test creating an ingredient is successful."""
        user = create_user()
        ingredient = Ingredient.objects.create(user=user, name="Ingredient1")

        self.assertEqual(str(ingredient), ingredient.name)

    @patch("core.models.uuid.uuid4")
    def test_recipe_file_neme_uuid(self, mock_uuid):
        """Test gentating imge path."""
        uuid = "test-uuid"
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, "example.jpg")

        self.assertEquals(file_path, f"uploads/recipe/{uuid}.jpg")
