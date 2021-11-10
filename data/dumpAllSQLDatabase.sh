#!/bin/bash
# Run this file to dump a MySQL backup file of everything
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"

/bin/bash ../bootleg-ebay/advertisements/db/dump.sh &
/bin/bash ../bootleg-ebay/users/db/dump.sh &
/bin/bash ../bootleg-ebay/payments/db/dump.sh &
wait 
echo "Done!"