#!/bin/bash
cd /app
if pytest /tests/test_stats.py -rA; then
  echo 1 > /logs/verifier/reward.txt
else
  echo 0 > /logs/verifier/reward.txt
fi
