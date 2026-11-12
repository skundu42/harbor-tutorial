#!/bin/bash
cat > /app/stats.py <<'EOF'
def median(values):
    """Return the median of a list of numbers."""
    values = sorted(values)
    n = len(values)
    mid = n // 2
    if n % 2 == 1:
        return values[mid]
    return (values[mid - 1] + values[mid]) / 2
EOF
