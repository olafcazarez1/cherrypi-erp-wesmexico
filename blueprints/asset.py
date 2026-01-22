import cherrypy
import logging
import json
import uuid

import os
import shutil

import time
from datetime import datetime
from PIL import Image
from utils.decorators import tools
from utils.singleton_meta import MetaConfig

from models.asset import Asset


class MapAsset(object):

    def __init__(self):
        meta = MetaConfig.instance()
        config = meta.get_config("asset")
        self.path = config["path"]

    def init(self, mapper=None):
        mapper.connect(
            "upload_asset",
            "/asset/upload",
            controller=self,
            action="upload_asset",
            conditions=dict(method=["POST", "OPTIONS"]),
        )

        mapper.connect(
            "get_asset",
            "/asset/{name}",
            controller=self,
            action="get_asset",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "get_asset_thumbnail",
            "/asset-thumbnail/{name}",
            controller=self,
            action="get_asset_thumbnail",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "delete_asset",
            "/asset/{name}",
            controller=self,
            action="delete_asset",
            conditions=dict(method=["DELETE", "OPTIONS"]),
        )

    @tools.cors
    @cherrypy.config(**{"response.timeout": 3600})
    @cherrypy.tools.json_out()
    def upload_asset(self, **kwargs):

        asset_id = kwargs.get("asset_id", str(uuid.uuid4()))

        name = kwargs.get("name", None)
        caption = kwargs.get("caption", None)
        typ = kwargs.get("type", None)
        file = kwargs.get("file", None)
        replace = kwargs.get("replace", False)

        if name is None:
            raise cherrypy.HTTPError(400, 'Invalid argument "name"')

        if caption is None:
            raise cherrypy.HTTPError(400, 'Invalid argument "caption"')

        if typ is None:
            raise cherrypy.HTTPError(400, 'Invalid argument "type"')

        if file is None:
            raise cherrypy.HTTPError(400, 'Invalid argument "file"')

        destination = "{}/{}{}".format(self.path, asset_id, os.path.splitext(name)[1])

        if os.path.isfile(destination):
            if not replace:
                raise cherrypy.HTTPError(
                    403,
                    "The asset already exist, use 'replace=True' to replace it",
                )

        """ Open File Destination """
        try:
            with open(destination, "wb") as fdst:
                shutil.copyfileobj(file.file, fdst)
        except IOError:
            raise cherrypy.HTTPError(507, "Insufficient Storage")

        size = 0
        height = 0
        width = 0

        if typ.startswith("image"):
            im = Image.open(destination)
            width, height = im.size
            size = len(im.fp.read())
        else:
            size = os.path.getsize(destination)

        asset = Asset()
        asset.asset_id = asset_id
        asset.name = "{}{}".format(asset_id, os.path.splitext(name)[1])
        asset.caption = name
        asset.path = destination
        asset.type = typ
        asset.height = height
        asset.width = width
        asset.size = size
        asset.created_at = datetime.utcnow()
        asset.updated_at = datetime.utcnow()
        asset.update_or_insert()

        data = asset.as_dict()
        data["url"] = "{}/{}".format("resources/assets", asset.name)
        del data["path"]
        return data

    @tools.cors
    def get_asset(self, **kwargs):

        name = kwargs.get("name")
        asset_id = os.path.splitext(name)[0]

        asset = Asset().where({"asset_id": asset_id}).one_or_none()

        if asset is None:
            raise cherrypy.HTTPError(404, "Not Found")

        if not os.path.exists(asset.path):
            raise cherrypy.HTTPError(404, "Not Found")

        return cherrypy.lib.static.serve_file(asset.path)

    @tools.cors
    def get_asset_thumbnail(self, **kwargs):

        name = kwargs.get("name")
        width = kwargs.get("width", 256)
        height = kwargs.get("height", 256)
        quality = kwargs.get("quality", 256)

        asset_id = os.path.splitext(name)[0]

        destination = "{}/{}{}".format(self.path, asset_id, os.path.splitext(name)[1])

        if not os.path.exists(destination):
            raise cherrypy.HTTPError(404, "Not Found")

        outfile_thumbnail = "/tmp/" + str(int(time.time())) + "_" + name
        try:
            img = Image.open(destination)
            img = img.resize((int(width), int(height)), Image.ANTIALIAS)
            # img.thumbnail([width, height])
            img.save(outfile_thumbnail, img.format, quality=int(quality))
        except IOError:
            raise cherrypy.HTTPError(507, "Insufficient Storage")

        return cherrypy.lib.static.serve_file(outfile_thumbnail)

    @tools.cors
    def delete_asset(self, **kwargs):

        name = kwargs.get("name")
        asset_id = os.path.splitext(name)[0]

        asset = Asset().where({"asset_id": asset_id}).one_or_none()

        if asset is None:
            return {}

        if os.path.exists(asset.path):
            os.remove(asset.path)

        asset.status = "deleted"
        asset.updated_at = datetime.utcnow()
        asset.update()

        return {}
