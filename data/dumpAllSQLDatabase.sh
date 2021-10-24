#!/bin/bash
# Run this file when you did git pull to sync ALL the latest changes into your SQL DBs
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"

/bin/bash ../bootleg-ebay/advertisements/db/dump.sh
/bin/bash ../bootleg-ebay/users/db/dump.sh