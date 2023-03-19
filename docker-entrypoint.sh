#!/bin/bash
echo "Applying Django Migrations"
./stackunderflow/manage.py migrate
echo "Migrations Applied successfully"
exec "$@"