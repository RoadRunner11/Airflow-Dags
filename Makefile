# Cleaning up the python compiled bytecodes
clear-pyc:
	find . | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs rm -rf

# Backup the database into file
dumpdb:
	pg_dump -U username -h host -p port dbname > dbname_20191005.dump

# Restore
restoredb:
	psql dbname < dbname_20191005.dump