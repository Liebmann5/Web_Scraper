#!/bin/bash

# Create the logging directory
mkdir -p logging

cd logging

# Create the external_node subdirectory
mkdir -p external_node

cd external_node

# Create the subdirectories
mkdir -p tasks templates

cd tasks

cat <<'EOL' > main.yml
---
# Deploy fluentbit
- name: Deploy fluentbit.
  include_role:
    name: liebmann5.fluentbit
  vars:
    # lua scripts
    fluentbit_lua_scripts:
      - name: adjust_ts.lua
        content: "{{ lookup('template','templates/adjust_ts.lua') }}"
EOL

cd ..

cd templates

cat <<'EOL' > adjust_ts.lua
function local_timestamp_to_UTC(tag, timestamp, record)
    local utcdate   = os.date("!*t", ts)
    local localdate = os.date("*t", ts)
    localdate.isdst = false -- this is the trick
    utc_time_diff = os.difftime(os.time(localdate), os.time(utcdate))
    return 1, timestamp - utc_time_diff, record
end
EOL

cd ../../..

chmod +x logging/external_node/tasks/main.yml
chmod +x logging/external_node/templates/adjust_ts.lua