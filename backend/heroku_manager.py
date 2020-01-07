import os
import sys

try:
   input = raw_input
except NameError:
   pass

if len(sys.argv) < 2:
    print("Usage: python3 heroku_manager.py [option]")
    print("Options:")
    print("    shell       open dyno bash shell")
    print("    push        push docker container")
    print("    psql        open postgres shell")
    print("    drop_db     drop all tables on db")
    print("    init_db     init tables and superuser")
    print("    db_size     get size of the db")
    print("")
    exit(0)

if sys.argv[1] == "shell":
    os.system("heroku run /bin/bash --app carbonara-backend")
elif sys.argv[1] == "push":
    os.system("cd ../frontend; npm run build")
    os.system("heroku container:push web --app carbonara-backend")
elif sys.argv[1] == "psql":
    os.system("psql ***")
elif sys.argv[1] == "drop_db":
    r = input("Are you sure? (Y, n) ")
    if r.lower() != "y":
        exit(0)
    print("Kill -9 tables...")
    os.system("printf 'drop schema public cascade;\ncreate schema public;\n' | psql ***")
elif sys.argv[1] == "init_db":
    os.system("env DATABASE_URL=*** python3 api/lshforest/init_db.py")
    os.system("heroku run 'python manage.py migrate' --app carbonara-backend")
    os.system("heroku run 'python manage.py createsuperuser' --app carbonara-backend")
elif sys.argv[1] == "db_size":
    os.system("echo 'SELECT pg_size_pretty(pg_database_size(current_database()));' | psql ***")


