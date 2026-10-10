import threading
import subprocess
import sys

class Run:
    def __init__(self, path, arguments, logger, javapath):
        self.process = None
        self.path = path
        self.arguments = arguments
        self.logger = logger
        self.javapath = javapath
        self.runnning = False
        self.thread = threading.Thread(target=self.runthread)

    def run(self):
        thread = threading.Thread(target=self.runthread)
        thread.start()

    def runthread(self):
        try:
            self.logger.write(f"Running server jar from: '{self.javapath}'", "INFO", "Run")
            self.runnning = True

            args = [self.javapath]
            for i in self.arguments:
                args.append(i)
            self.process = subprocess.Popen(args,cwd=self.path, stdin=subprocess.PIPE ,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            for line in self.process.stdout:
                self.logger.write(line.decode("ascii").replace("\n", ""), "INFO", "Minecraft")
                if "Preparing spawn area: 100%" in line.decode("ascii"):
                    self.runnning = True

            returncode = self.process.wait()
            if returncode != 0:
                raise subprocess.CalledProcessError(returncode, self.process.args)

            self.runnning = False
        except Exception as e:
            self.logger.write(f"Running server jar failed: {e}", "ERROR", "Run")
            self.runnning = False

    def toogle_run(self):
        if self.runnning:
            self.logger.write(f"Shutting down server", "INFO", "Run")
            self.write(b'stop')
            return "OFFLINE"
        else:
            self.logger.write(f"Running server", "INFO", "Run")
            self.run()
            return "ONLINE"


    def write(self, text):
        self.logger.write(f"Writing to server console", "INFO", "Run")
        try:

            # o = self.process.communicate(input=text)[0]
            self.process.stdin.write(text + b'\n')
            self.process.stdin.flush()
        except Exception as e:
            self.logger.write(f"Writing to server console failed: {e}", "ERROR", "Run")

