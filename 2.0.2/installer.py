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
        self.logger= logging_module.Logging(True, self.get_logs_from_logger) # Logging object
        self.logs = "" # Logs variable

        self.config = self.load_config() # Configuration file
        self.dependencies = self.load_dependencies() # Dependencies file

        self.java_path = "" # Java path

        self.app = Flask(__name__, static_folder='installer_web/static',template_folder='installer_web/templates') # Flask object
        self.server = create_server(self.app, host="127.0.0.1", port=80) # Waitress object
        self.logger.write("Installer-web is running on: http://127.0.0.1:80", "INFO", "Installer-web") # Write to the log

        self.declare_url()



    # Run web server
    def run(self):
        self.server.run()

    # Load config
    def load_config(self):
        self.logger.write("Loading config file", "INFO", "Config")
        try:
            with open("configuration.json", "r") as raw_file:
                return json.load(raw_file)
        except Exception as e:
            self.logger.write(f"Loading config failed: {e}", "ERROR", "Config")

    # Load dependencies
    def load_dependencies(self):
        self.logger.write("Loading dependencies file", "INFO", "Dependencies")
        try:
            with open("dependencies.json", "r") as raw_file:
                return json.load(raw_file)
        except Exception as e:
            self.logger.write(f"Loading dependencies failed: {e}", "ERROR", "Dependencies")

    def declare_url(self):
        self.app.add_url_rule("/", view_func=self.main)
        self.app.add_url_rule("/install/", view_func=self.install)
        self.app.add_url_rule("/getData/", view_func=self.get_data)
        self.app.add_url_rule("/getLogs/", view_func=self.get_logs)
        self.app.add_url_rule("/postData/", view_func=self.post_data, methods=["POST"])
        self.app.add_url_rule("/postIcon/", view_func=self.post_icon, methods=["POST"])

    @staticmethod
    def main():
        return render_template("main.html") # Render main page

    @staticmethod
    def install():
        return render_template("install.html") # Render logs page

    def get_data(self):
        with open("dependencies.json", "r") as raw_file:
            return json.dumps(raw_file.read()), 200


    def get_logs(self):
        return self.logs, 200 # Return logs

    def post_data(self):
        self.logger.write(f"Posted data are: {request.data}", "DEBUG", "Web-installer")
        thread = threading.Thread(target=self.install_server, args=[request.json,]) # Create thread
        thread.start() # Run thread
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

    def install_server(self, data):
        time.sleep(2) # Wait 2 seconds
        if data is not None:
            self.logs = "" # Logs
            name = data.get("name").replace(" ", "_") # Server name

            # Install Java
            for i in self.dependencies["java"]:
                if data.get("java") in i["version"]:
                    obj = install_java.InstallJava(self.logger, self.config["java_path"], i[sys.platform]) # Create Java installer obj
                    obj.download_java() # Download Java
                    self.java_path = obj.get_java_directory() # Gets the Java path


            # Install MC Server
            for version in self.dependencies["modloader"][data.get("modloader")]:
                if data.get("version") in version["version"]:
                    install_server.InstallServer(version["url"],os.path.join(self.config["server_path"],name),self.logger, self.java_path,version["install_command"],name, data.get("ram"),data.get("motd"),data.get("ip"))
                    os.kill(os.getpid(), signal.SIGILL) # Kill install web

            self.logger.write(f"The Java version is not in the posted data: {data}", "WARN", "Web-installer")




