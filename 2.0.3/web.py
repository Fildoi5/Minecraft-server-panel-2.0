import json
import threading
import random
import time
import auto_start
import pswd

import psutil

from waitress.server import create_server

from flask import Flask, render_template, request, redirect, url_for, session
import logging_module
import run

class Web:
    def __init__(self):
        self.logger= logging_module.Logging(True, self.get_logs_from_logger, "Minecraft") # Logger object
        self.logs_str = "" # Logs

        self.status = {
            "status" : "OFFLINE",
            "ram" : "0 GB",
            "cpu": "0%"
        }

        self.auto_start_obj = auto_start.AutoStart(self.logger)

        self.usage_p = threading.Thread(target=self.get_usage)
        self.usage_p.start()

        self.server_data = self.load_server_data() # Load server data

        self.pswd_object = pswd.Pswd(self.logger)

        self.creating_user = False

        self.users = {

        }

        self.run_server_obj = run.Run(self.server_data["path"],["-jar","server.jar"],self.logger, self.server_data["java_path"])

        self.app = Flask(__name__, static_folder='main_web/static',template_folder='main_web/templates')
        self.app.secret_key = "%032x" % random.getrandbits(128)
        self.server = create_server(self.app, host="127.0.0.1", port=80,threads=6)
        self.logger.write(r"Web is running on: http://127.0.0.1:80", "INFO", "Web")

        self.declare_url()


    # Run waitress server
    def run(self):
        self.server.run()

    # Load server data
    def load_server_data(self):
        self.logger.write("Loading server data file", "INFO", "Server Data")
        try:
            with open("server.json", "r") as raw_file:
                return json.load(raw_file)
        except Exception as e:
            self.logger.write(f"Loading server data failed: {e}", "ERROR", "Server Data")


    # Measures RAM and CPU usage
    def get_usage(self):
        while True:

            cpu = str(psutil.cpu_percent())
            self.status["cpu"] = cpu + "%"
            self.status["ram"] = str(psutil.virtual_memory().percent) + "%"

            if self.auto_start_obj.check_startup_time():
                self.run_server_obj.toogle_run("On")

            if self.auto_start_obj.check_shutdown_time():
                self.run_server_obj.toogle_run("Off")

            time.sleep(1) # Wait 1 second

    def declare_url(self):
        self.app.add_url_rule("/", view_func=self.main)
        self.app.add_url_rule("/logs", view_func=self.logs)
        self.app.add_url_rule("/stats", view_func=self.stats)
        self.app.add_url_rule("/settings", view_func=self.settings)
        self.app.add_url_rule("/get_logs", view_func=self.get_logs, methods=["GET"])
        self.app.add_url_rule("/get_data", view_func=self.get_data, methods=["GET"])
        self.app.add_url_rule("/get_time", view_func=self.get_time, methods=["GET"])
        self.app.add_url_rule("/login", view_func=self.login, methods=["GET","POST"])
        self.app.add_url_rule("/create_user", view_func=self.create_user, methods=["GET", "POST"])
        self.app.add_url_rule("/postPower", view_func=self.post_power, methods=["POST"])
        self.app.add_url_rule("/postWrite", view_func=self.post_write, methods=["POST"])
        self.app.add_url_rule("/postTime", view_func=self.post_time, methods=["POST"])


    def get_logs_from_logger(self, logs):

        list = self.logs_str.split("\n")
        if len(list) > 100:
            self.logs_str = ""
            list.pop(0) # Deletes the first item from the list
            for log in list:
                self.logs_str += log + "\n"
            self.logs_str += logs
        else:
            self.logs_str += logs + "\n"


    def main(self):
        if session.get("id") == self.users.get("admin") and session.get("id") is not None: # Verifies whether the user is logged in.
            return render_template("main.html") # Render main page
        return redirect("/login") # Redirect to login page

    def logs(self):
        if session.get("id") == self.users.get("admin") and session.get("id") is not None: # Verifies whether the user is logged in.
            return render_template("logs.html")
        return redirect("/login") # Redirect to login page


    def stats(self):
        if session.get("id") == self.users.get("admin") and session.get("id") is not None: # Verifies whether the user is logged in.
            return render_template("stats.html")
        return redirect("/login") # Redirect to login page

    def settings(self):
        if session.get("id") == self.users.get("admin") and session.get("id") is not None: # Verifies whether the user is logged in.
            return render_template("settings.html")
        return redirect("/login") # Redirect to login page

    def login(self):
        msg = ''
        if self.pswd_object.exist():
            if request.method == 'POST' and 'username' in request.form and 'password' in request.form:

                username = request.form['username']
                password = request.form['password']

                self.logger.write(f"Password: {password}", "DEBUG", "Web")
                self.logger.write(f"Username: {username}", "DEBUG", "Web")

                if self.pswd_object.check_pswd(username,password):
                    hash = "%032x" % random.getrandbits(128) # Create random hash
                    self.users["admin"] = hash

                    self.logger.write(f"Users: {self.users}", "DEBUG", "Web")

                    session['id'] = hash
                    session['username'] = username

                    return redirect(url_for("main"))
                else:
                    msg = 'Incorrect username/password!'

            return render_template('login.html', msg=msg)
        else:
            return redirect(url_for("create_user"))

    def create_user(self):
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']

            self.logger.write(f"New password: {password}", "DEBUG", "Web")
            self.logger.write(f"New username: {username}", "DEBUG", "Web")

            self.pswd_object.create(password,username)

            return redirect(url_for("login"))

        return render_template('create_user.html')

    def post_power(self):
        if session.get("id") == self.users.get("admin") and session.get("id") is not None: # Verifies whether the user is logged in.

            self.status["status"] = self.run_server_obj.toogle_run()
            return "", 200
        return "", 401 # Return code 401

    def post_write(self):
        if session.get("id") == self.users.get("admin") and session.get("id") is not None: # Verifies whether the user is logged in.
            self.run_server_obj.write(request.data)

            return "", 200
        return "", 401 # Return code 401

    def post_time(self):
        if session.get("id") == self.users.get("admin") and session.get("id") is not None: # Verifies whether the user is logged in.
            self.auto_start_obj.create_own_config(request.json)

            return "", 200
        return "", 401 # Return code 401

    def get_data(self):
        if session.get("id") == self.users.get("admin") and session.get("id") is not None: # Verifies whether the user is logged in.
            return json.dumps(self.status), 200
        return "", 401 # Return code 401

    def get_logs(self):
        if session.get("id") == self.users.get("admin") and session.get("id") is not None: # Verifies whether the user is logged in.
            return self.logs_str, 200 # Return logs
        return "", 401 # Return code 401

    def get_time(self):
        if session.get("id") == self.users.get("admin") and session.get("id") is not None: # Verifies whether the user is logged in.
            return self.auto_start_obj.load_config(), 200
        return "", 401 # Return code 401

