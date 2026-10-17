import hashlib
import os
import json
import random

class Pswd:
    def __init__(self, logger):
        self.logger = logger
        self.path = os.path.join(os.getcwd(),"pswd.json")
    def create(self, raw_password, user):
        self.logger.write("Creating file", "INFO", "Pswd")
        try:
            salt = self.get_random_salt()
            dic = {"user": user, "hash": self.get_hash(raw_password,salt), "salt": salt}

            # Write to pswd.json
            with open(self.path,"w") as file:
                json.dump(dic,file) # Write json

        except Exception as e:
            self.logger.write("Creating file faild", "ERROR", "Pswd")
    def get_hash(self, raw_password, salt):
        self.logger.write("Creating hash", "INFO", "Pswd")
        raw = raw_password + salt

        return hashlib.sha256(raw.encode("utf-8")).hexdigest() # Return hash

    def get_random_salt(self):
        self.logger.write("Creating random salt", "INFO", "Pswd")
        alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        chars = []
        for i in range(16):
            chars.append(random.choice(alphabet))

        salt = "".join(chars)

        return salt

    def check_pswd(self, user, password):
        self.logger.write("Checking pswd", "INFO", "Pswd")
        try:
            with open(self.path, "r") as file:
                dic = json.load(file)

                if dic.get("user") == user:
                    pswd_hash = self.get_hash(password, dic.get("salt"))
                    if pswd_hash == dic.get("hash"):
                        return True
                    else:
                        return False
                return False
        except Exception as e:
            self.logger.write("Checking pswd faild", "ERROR", "Pswd")

    def exist(self):
        return os.path.exists(self.path)