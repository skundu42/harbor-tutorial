#!/bin/bash
cat > /app/query.sql <<'EOF'
SELECT c.name
FROM customers c JOIN orders o ON o.customer_id = c.id
GROUP BY c.id
ORDER BY SUM(o.amount) DESC
LIMIT 1;
EOF
