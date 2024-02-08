import os
import uuid

from celery.result import AsyncResult
from flask import Flask, jsonify, request
from flask.views import MethodView
from tasks import celery_app, upscale

app = Flask("app")
app.config["UPLOAD_FOLDER"] = "files"
celery_app.conf.update(app.config)


class ContextTask(celery_app.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)


celery_app.Task = ContextTask


class Upscale(MethodView):
    @staticmethod
    def get(task_id):
        task = AsyncResult(task_id, app=celery_app)
        return jsonify({"status": task.status, "result": task.result})

    def post(self):
        path_in, path_out = self.save_image()
        task = upscale.delay(path_in, path_out)
        return jsonify({"task_id": task.id, "file": path_out})

    @staticmethod
    def save_image():
        image = request.files.get("files")
        extension = image.filename.split(".")[-1]
        path_in = os.path.join("files", f"{uuid.uuid4()}_in.{extension}")
        path_out = os.path.join("files", f"{uuid.uuid4()}_out.{extension}")
        image.save(path_in)
        return path_in, path_out


class Processed(MethodView):
    @staticmethod
    def get(file):
        status = "ERROR"
        if file:
            status = "SUCCESS"
        return jsonify(
            {"status": status, "result_path": os.path.join("files", f"{file}")}
        )


upscale_view = Upscale.as_view("upscale")
processed_view = Processed.as_view("processed")

app.add_url_rule("/tasks/<string:task_id>", view_func=upscale_view, methods=["GET"])
app.add_url_rule("/processed/<string:file>", view_func=processed_view, methods=["GET"])
app.add_url_rule("/upscale/", view_func=upscale_view, methods=["POST"])


if __name__ == "__main__":
    app.run()
