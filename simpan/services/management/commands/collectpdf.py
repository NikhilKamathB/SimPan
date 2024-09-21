import os
import shutil
import logging
from django.conf import settings
from django.core.management.base import BaseCommand


LOGGER = logging.getLogger(__name__)


class Command(BaseCommand):

    help = "Move `pdf.js` statics to `settings.STATIC_BASE`"

    def handle(self, *args, **options) -> None:
        if not os.path.exists(os.path.join(settings.SUBMODULES_DIR, settings.PDF_DIR)):
            LOGGER.warning("`PDF.js` submoudle not found.")
            return
        if not os.path.exists(os.path.join(settings.SUBMODULES_DIR, settings.PDF_DIR, "build")):
            LOGGER.warning("`build` directory not found in `PDF.js` submoudle.")
            return
        try:
            LOGGER.info("Copying `PDF.js` build items to `settings.STATIC_BASE`")
            os.makedirs(os.path.join(settings.BASE_DIR, settings.STATIC_BASE), exist_ok=True)
            # Copy pdf - build js files
            shutil.copytree(
                os.path.join(settings.SUBMODULES_DIR, settings.PDF_DIR, "build", "generic", "build"),
                os.path.join(settings.BASE_DIR, settings.STATIC_BASE, "js"), dirs_exist_ok=True
            )
        except Exception as e:
            LOGGER.error(f"Error copying `PDF.js` statics to `settings.STATIC_BASE`: {e}")
            return