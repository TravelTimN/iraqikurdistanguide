import os
import datetime
from slugify import slugify
from django.db import models
from django.conf import settings
from PIL import Image, ImageOps
import destinations.models


def upload_to(instance, filename):
    """
        Slugify the destination/ and sight/ plus YYMMDD-HHMMSS .webp
    """
    sight_slug = slugify(instance.sight.destination.name)
    file_name = slugify(instance.sight.name)
    now = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
    file_slug = slugify(file_name)
    # set the Model instance of the image
    instance.image = f"uploads/{sight_slug}/{file_slug}-{now}.webp"
    return f"uploads/{sight_slug}/{file_slug}-{now}.webp"


class Photo(models.Model):
    """
        Allows admins to upload new images, to be used as FKs
        for destinations, sites, tours, etc.
    """
    sight = models.ForeignKey(
        "destinations.Sight", on_delete=models.CASCADE, null=False, blank=False)
    image = models.ImageField(
        default="no-image.png",
        upload_to=upload_to,
        unique=True,
        blank=False,
        null=False)
    caption = models.CharField(max_length=250, null=False, blank=False)
    is_visible = models.BooleanField(default=True)

    def image_preview(self):
        from django.utils.html import format_html
        return format_html(f"<img src='{self.image.url}' height='150'>")

    class Meta:
        ordering = ["sight__destination", "sight__name", "image"]

    def __str__(self):
        return self.sight.name

    def save(self, *args, **kwargs):
        """
        - installed 'django-cleanup' to auto-remove old image.
        - installed 'pillow' to compress image sizes.
        - above does not apply to .gif files.
        """
        super(Photo, self).save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image)
            # continue if image format is not .gif
            if img.format.lower() != "gif":

                # https://github.com/python-pillow/Pillow/issues/4703#issuecomment-645219973
                img = ImageOps.exif_transpose(img)  # prevent auto-rotate 90°

                # https://stackoverflow.com/a/53644302
                img = img.convert("RGB")  # required for .webp

                # get image file size
                img_size = int(os.stat(self.image.path).st_size)

                # generate upload_to file-location (if updating image)
                img_name = upload_to(self, self.image)
                img_path = f"{settings.MEDIA_ROOT}/{img_name}"
                destination = img_name.split("/")[1]
                img_dir = f"{settings.MEDIA_ROOT}/uploads/{destination}"

                # check if destination/ dir already exists; create it, if not
                if not os.path.exists(img_dir):
                    os.mkdir(img_dir)
                mib = 1048576  # 1MiB = 1048576 bytes

                # save Photo model instance and image
                if img_size > mib:
                    # if filesize >1MiB, compress image and save
                    img.save(img_path, img.format, quality=50, optimize=True)
                else:
                    # no compression, but save original quality
                    img.save(img_path, img.format)

                super(Photo, self).save(*args, **kwargs)
