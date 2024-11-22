from rest_framework import status
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from file_manager.models import UploadedFile


class FileUploadTests(APITestCase):

    def test_upload_file(self):
        """
        Test uploading a file.
        """
        file_data = SimpleUploadedFile(
            "test.pdf", b"file_content", content_type="application/pdf"
        )

        response = self.client.post(
            "/api/upload/", {"file": file_data}, format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)  # Check that the file ID is returned
        self.assertEqual(response.data["file_type"], "pdf")

    def test_upload_large_file(self):
        """
        Test uploading a file that's too large (should be rejected).
        """

        large_file = SimpleUploadedFile(
            "large_test.pdf",
            b"file_content" * 1024 * 1024,
            content_type="application/pdf",
        )

        response = self.client.post(
            "/api/upload/", {"file": large_file}, format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "File size exceeds 5 MB limit.")

    def test_list_files(self):
        """
        Test listing all uploaded files.
        """
        file_data = SimpleUploadedFile(
            "test1.pdf", b"file_content", content_type="application/pdf"
        )
        self.client.post("/api/upload/", {"file": file_data}, format="multipart")

        file_data2 = SimpleUploadedFile(
            "test2.jpg", b"file_content", content_type="image/jpg"
        )
        self.client.post("/api/upload/", {"file": file_data2}, format="multipart")

        response = self.client.get("/api/files/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["file_type"], "pdf")
        self.assertEqual(response.data[1]["file_type"], "jpg")

    def test_list_files_by_type(self):
        """
        Test filtering files by type.
        """
        file_data1 = SimpleUploadedFile(
            "test1.pdf", b"file_content", content_type="application/pdf"
        )
        self.client.post("/api/upload/", {"file": file_data1}, format="multipart")
        file_data2 = SimpleUploadedFile(
            "test2.jpg", b"file_content", content_type="image/jpg"
        )
        self.client.post("/api/upload/", {"file": file_data2}, format="multipart")

        response = self.client.get("/api/files/?file_type=pdf")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["file_type"], "pdf")

    def test_retrieve_file(self):
        """
        Test retrieving a specific file by ID.
        """
        file_data = SimpleUploadedFile(
            "test.pdf", b"file_content", content_type="application/pdf"
        )
        response = self.client.post(
            "/api/upload/", {"file": file_data}, format="multipart"
        )
        file_id = response.data["id"]

        response = self.client.get(f"/api/files/{file_id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], file_id)
        self.assertEqual(response.data["file_type"], "pdf")

    def test_retrieve_nonexistent_file(self):
        """
        Test retrieving a non-existent file by ID.
        """
        response = self.client.get("/api/files/50/") 
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "File not found.")
