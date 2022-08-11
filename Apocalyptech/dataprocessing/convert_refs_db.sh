#!/bin/bash
# vim: set expandtab tabstop=4 shiftwidth=4:
# read -sp 'Enter wlrefs pass: ' FULLPASS
# read -sp 'Enter wlrefs_ro pass: ' PASS
echo "Reading settings from local-settings-rc"
source local-settings-rc
echo
echo "Dumping SQL first..."
echo
rm wlrefs.zip
# Might have to make -p optional
mysqldump -u ${USER} -p${FULLPASS} -h${HOST} -P${PORT} wlrefs > wlrefs.sql
zip wlrefs.zip wlrefs.sql
rm wlrefs.sql
echo
echo "Now doing SQLite dump/conversion..."
echo
rm wlrefs.sqlite3*
# Might have to make -P optional
${MYSQL2SQLITE} -f wlrefs.sqlite3 -d wlrefs -u ${USER} -h ${HOST} -P ${PORT} -V --mysql-password ${PASS} && zip wlrefs.sqlite3.zip wlrefs.sqlite3 && ls -lh wlrefs.sqlite3*
ls -lh wlrefs.zip
