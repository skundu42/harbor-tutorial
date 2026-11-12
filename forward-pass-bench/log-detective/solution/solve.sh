#!/bin/bash
LOG=/app/server.log

errors=$(awk '$5 >= 500' $LOG | wc -l)
top_ip=$(awk '{print $2}' $LOG | sort | uniq -c | sort -rn | head -1 | awk '{print $2}')
slowest=$(sort -k6 -rn $LOG | head -1 | awk '{print $4}')

printf '{"errors": %d, "top_ip": "%s", "slowest_path": "%s"}\n' \
  "$errors" "$top_ip" "$slowest" > /app/answer.json
