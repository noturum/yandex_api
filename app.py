import asyncio
import os
from flask import Flask, render_template, request, jsonify, send_file
from client.YandexApi import YandexApi
from client.types import DownloadsFile
from client.types import MediaType
from flask_caching import Cache

app = Flask(__name__)
config = {'CACHE_TYPE': 'SimpleCache', 'CACHE_DEFAULT_TIMEOUT': 60 * 60}

cache = Cache(app, config=config)


@app.route("/", methods=["GET", "POST"])
async def index():
    return render_template("index.html")


@app.route("/files", methods=["POST"])
async def get_file_list():
    data = request.get_json()
    public_key = data.get("public_key")
    path = data.get('path')
    _filter = data.get('filter')
    file_list = await YandexApi.get_file_list(public_key, path)
    if _filter and _filter != MediaType.ALL:
        file_list = YandexApi.filter(file_list, _filter)
    file_list = [file.model_dump() for file in file_list]
    return jsonify(
        file_list
    )


@app.route("/download", methods=["POST"])
async def download_list():
    files = []
    file_list = DownloadsFile.model_validate(
        request.json
    ).files
    for url in file_list:
        files.append(
            await YandexApi.downloads_file(
                url.file_path,
                './download/' + url.file_name,
            )
        )
    return files


@app.route("/download/<filename>")
def download_from_server(filename):
    file_path = os.path.join("download", filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return "File not found", 404


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8081,
    )
