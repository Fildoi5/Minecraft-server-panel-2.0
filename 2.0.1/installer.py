import os
import json
import signal
import sys
import threading
import time

from waitress.server import create_server
from flask import Flask, render_template, request

import install_java
import install_server
import logging_module

class Installer:
    def __init__(self):

        self.logger= logging_module.Logging(True, self.get_logs_from_logger)
        self.logs = ""


        self.config = self.load_config()
        self.dependencies = self.load_dependencies()

        self.java_path = ""

        self.app = Flask(__name__, static_folder='installer_web/static',template_folder='installer_web/templates')
        self.server = create_server(self.app, host="127.0.0.1", port=80)
        self.logger.write("Installer-web is running on: http://127.0.0.1:80", "INFO", "Installer-web")



        self.declare_url()




    def run(self):
        self.server.run()

        # self.app.run(port=5000)

    def load_config(self):
        self.logger.write("Loading config file", "INFO", "Config")
        try:
            with open("configuration.json", "r") as raw_file:
                return json.load(raw_file)
        except Exception as e:
            self.logger.write(f"Loading config failed: {e}", "ERROR", "Config")
            sys.exit()

    def load_dependencies(self):
        self.logger.write("Loading dependencies file", "INFO", "Dependencies")
        try:
            with open("dependencies.json", "r") as raw_file:
                return json.load(raw_file)
        except Exception as e:
            self.logger.write(f"Loading dependencies failed: {e}", "ERROR", "Dependencies")
            sys.exit()

    def declare_url(self):
        self.app.add_url_rule("/", view_func=self.main)
        self.app.add_url_rule("/install/", view_func=self.install)
        self.app.add_url_rule("/getData/", view_func=self.get_data)
        self.app.add_url_rule("/getLogs/", view_func=self.get_logs)
        self.app.add_url_rule("/postData/", view_func=self.post_data, methods=["POST"])
        self.app.add_url_rule("/postIcon/", view_func=self.post_icon, methods=["POST"])

    @staticmethod
    def main():
        return render_template("main.html")

    @staticmethod
    def install():
        return render_template("install.html")

    def get_data(self):
        with open("dependencies.json", "r") as raw_file:
            return json.dumps(raw_file.read()), 200


    def get_logs(self):
        return self.logs, 200

    def post_data(self):
        self.logger.write(f"Requested data are: {request.data}", "DEBUG", "Web-installer")
        thread = threading.Thread(target=self.install_server, args=[request.json,request.data,])
        thread.start()
        return "", 200

    def post_icon(self):
        if request.data is not None:
            with open("img.png", "wb") as image:
                image.write(request.data)
            return "", 200
        else:
            return "", 204

    def get_logs_from_logger(self, logs):
        self.logs += logs + "\n"

    def install_server(self, json,data):
        time.sleep(2)
        if data is not None: #not
            jdata = json
            self.logs = ""
            name = jdata["name"].replace(" ", "_")

            for i in self.dependencies["java"]:
                if jdata["java"] in i["version"]:
                    obj = install_java.InstallJava(self.logger, self.config["java_path"], i[sys.platform])
                    obj.download_java()
                    self.java_path = obj.get_java_directory()

            for i in self.dependencies["modloader"][jdata["modloader"]]:
                if jdata["version"] in i["version"]:
                    install_server.InstallServer(i["url"],os.path.join(self.config["server_path"],name),self.logger, self.java_path,i["install_command"], i,name, jdata["ram"])
                    os.kill(os.getpid(), signal.SIGILL)

            self.logger.write(f"The Java version is not in the posted data: {jdata}", "WARN", "Web-installer")




