from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.Note.models import NoteModel


class NoteOwnershipTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.owner = user_model.objects.create_user(
            username="note-owner",
            password="test-password",
        )
        self.other_user = user_model.objects.create_user(
            username="other-user",
            password="test-password",
        )
        self.owned_note = self.create_note(self.owner, "Private note")
        self.other_note = self.create_note(self.other_user, "Someone else's note")
        self.client.force_login(self.owner)

    def create_note(self, owner, title):
        return NoteModel.objects.create(
            title=title,
            author=owner.username if owner else "Unknown",
            Text="Note content",
            description="",
            owner=owner,
        )

    def test_notes_list_only_shows_owned_notes(self):
        response = self.client.get(reverse("notes"))

        self.assertContains(response, self.owned_note.title)
        self.assertNotContains(response, self.other_note.title)

    def test_notes_list_hides_notes_without_an_owner(self):
        unowned_note = self.create_note(None, "Unassigned legacy note")
        response = self.client.get(reverse("notes"))

        self.assertNotContains(response, unowned_note.title)

    def test_user_cannot_view_another_users_note(self):
        response = self.client.get(
            reverse("notes_details", args=[self.other_note.id])
        )

        self.assertEqual(response.status_code, 404)

    def test_user_cannot_update_another_users_note(self):
        response = self.client.post(
            reverse("notes_update", args=[self.other_note.id]),
            {"title": "Changed title"},
        )

        self.assertEqual(response.status_code, 404)
        self.other_note.refresh_from_db()
        self.assertEqual(self.other_note.title, "Someone else's note")

    def test_user_cannot_delete_another_users_note(self):
        response = self.client.get(
            reverse("notes_delete", args=[self.other_note.id])
        )

        self.assertEqual(response.status_code, 404)
        self.assertTrue(NoteModel.objects.filter(pk=self.other_note.pk).exists())

    def test_created_note_belongs_to_logged_in_user(self):
        response = self.client.post(
            reverse("note_create"),
            {
                "title": "New note",
                "author": self.owner.username,
                "Text": "New note content",
                "description": "",
            },
        )

        self.assertRedirects(response, reverse("notes"))
        note = NoteModel.objects.get(title="New note")
        self.assertEqual(note.owner, self.owner)
