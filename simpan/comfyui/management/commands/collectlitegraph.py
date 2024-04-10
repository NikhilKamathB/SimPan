import os
import shutil
import logging
from django.conf import settings
from django.core.management.base import BaseCommand


LOGGER = logging.getLogger(__name__)


class Command(BaseCommand):

    help = "Move `litegraph.js` statics to `settings.STATIC_BASE`"

    def handle(self, *args, **options) -> None:
        if not os.path.exists(os.path.join(settings.SUBMODULES_DIR, settings.LITEGRAPH_DIR)):
            LOGGER.warning("`Litegraph.js` submoudle not found.")
            return
        if not os.path.exists(os.path.join(settings.SUBMODULES_DIR, settings.LITEGRAPH_DIR, "build")):
            LOGGER.warning("`build` directory not found in `Litegraph.js` submoudle.")
            return
        if not os.path.exists(os.path.join(settings.SUBMODULES_DIR, settings.LITEGRAPH_DIR, "css")):
            LOGGER.warning("`css` directory not found in `Litegraph.js` submoudle.")
            return
        try:
            LOGGER.info("Copying `litegraph.js` statics to `settings.STATIC_BASE`")
            os.makedirs(os.path.join(settings.BASE_DIR, settings.STATIC_BASE), exist_ok=True)
            # Copy js files
            shutil.copytree(
                os.path.join(settings.SUBMODULES_DIR, settings.LITEGRAPH_DIR, "build"),
                os.path.join(settings.BASE_DIR, settings.STATIC_BASE, "js"), dirs_exist_ok=True
            )
            # Copy css files
            shutil.copytree(
                os.path.join(settings.SUBMODULES_DIR, settings.LITEGRAPH_DIR, "css"),
                os.path.join(settings.BASE_DIR, settings.STATIC_BASE, "css"), dirs_exist_ok=True
            )
        except Exception as e:
            LOGGER.error(f"Error copying `litegraph.js` statics to `settings.STATIC_BASE`: {e}")
            return