#!/bin/bash
# Run this file when you did git pull to sync ALL the latest changes into your Mongo DBs
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"

/bin/bash ../bootleg-ebay/auctions/db/import.sh &
/bin/bash ../bootleg-ebay/items/db/import.sh &
/bin/bash ../bootleg-ebay/notifs/db/import.sh &
wait
echo "Done!"

