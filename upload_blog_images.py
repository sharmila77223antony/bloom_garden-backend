
import os
import django
from pathlib import Path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog.settings")
django.setup()

from django.conf import settings
import cloudinary
import cloudinary.uploader

cloudinary.config(
    cloud_name=settings.CLOUDINARY_STORAGE["CLOUD_NAME"],
    api_key=settings.CLOUDINARY_STORAGE["API_KEY"],
    api_secret=settings.CLOUDINARY_STORAGE["API_SECRET"],
    secure=True,
)

image_folder = Path(settings.BASE_DIR) / "media" / "blogs"

images = ["flower1.jpg", "flower2.jpg"]

for filename in images:
    file_path = image_folder / filename

    if not file_path.exists():
        print(f"FILE NOT FOUND: {file_path}")
        continue

    try:
        result = cloudinary.uploader.upload(
            str(file_path),
            public_id=f"blogs/{file_path.stem}",
            overwrite=True,
            resource_type="image",
        )

        print(f"\nUploaded successfully: {filename}")
        print("Public ID:", result["public_id"])
        print("Image URL:", result["secure_url"])

    except Exception as error:
        print(f"\nUpload failed for {filename}: {error}")
