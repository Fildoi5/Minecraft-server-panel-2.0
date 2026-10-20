import os.path
import sys
import threading
import subprocess

class Run:
    def __init__(self, path, arguments, logger, javapath):
        self.process = None # Server process
        self.path = path # Path to the working directory
        self.arguments = arguments # Arguments for launching
        self.logger = logger # Logger object
        self.javapath = javapath # Java path
        self.runnning = False
        self.default_args = None


    # Run function
    def run(self):
        thread = threading.Thread(target=self.runthread) # Server process thread
        thread.start() # Run thread

    def create_args(self):
        try:
            self.logger.write("Creating args", "INFO", "Run (create_args())") # Write to the log

            if sys.platform == "linux":
                with open(os.path.join(os.getcwd(),"user.usr"), "r") as file:
                    text = file.read()
                    if text.strip() != "":
                        return ["sudo","-u", text.strip()]
                    else:
                        return []
            else:
                return []
        except Exception as e:
            self.logger.write("Creating args failed", "ERROR", "Run (create_args())")  # Write to the log

    def runthread(self):
        try:
            self.logger.write(f"Running server jar from: '{self.javapath}'", "INFO", "Run") # Write to the log
            self.runnning = True

            # Set arguments
            args = self.create_args() + [self.javapath]
            for i in self.arguments:
                args.append(i)

            self.logger.write(f"Run args: '{args}'", "DEBUG", "Run")  # Write to the log


            self.process = subprocess.Popen(args,cwd=self.path, stdin=subprocess.PIPE ,stdout=subprocess.PIPE, stderr=subprocess.STDOUT) # Create process

            # Read stdout
            for line in self.process.stdout:
                self.logger.write(line.decode('utf-8').replace("\n", ""), "INFO", "Minecraft")# Write every line to the log
                if "Preparing spawn area: 100%" in line.decode('utf-8'):
                    self.runnning = True

            returncode = self.process.wait()
            if returncode != 0:
                raise subprocess.CalledProcessError(returncode, self.process.args)

            self.runnning = False
        except Exception as e:
            self.logger.write(f"Running server jar failed: {e}", "ERROR", "Run") # Write to the log
            self.runnning = False

    def toogle_run(self, power=None):
        if (self.runnning and power is None) or (power == "Off" and self.runnning):
            self.logger.write(f"Shutting down server", "INFO", "Run") # Write to the log
            self.write(b'stop')
            return "OFFLINE" # Returns that the server is down
        elif (not self.runnning and power is None)  or (power == "On" and not self.runnning):
            self.logger.write(f"Running server", "INFO", "Run") # Write to the log
            self.run() # Run server
            return "ONLINE" # Returns that the server is up
        return None

    def write(self, text):
        self.logger.write(f"Writing to server console", "INFO", "Run") # Write to the log
        try:
            self.process.stdin.write(text + b'\n')
            self.process.stdin.flush()
        except Exception as e:
            self.logger.write(f"Writing to server console failed: {e}", "ERROR", "Run") # Write to the log

