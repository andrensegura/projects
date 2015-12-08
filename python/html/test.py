from dbstructure import LOGGED_IN
import toml
with open("db.toml") as toml_file:
    config = toml.loads(toml_file.read())['database']['username']

print config
print LOGGED_IN
