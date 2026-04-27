#!/bin/bash
echo "=== /app directory ==="
ls -la /app/
echo ""
echo "=== /app/backend directory ==="
ls -la /app/backend/
echo ""
echo "=== /app/backend/app directory ==="
ls -la /app/backend/app/
echo ""
echo "=== Python path ==="
python3 -c "import sys; print('\n'.join(sys.path))"
echo ""
echo "=== Test import ==="
cd /app && python3 -c "import backend.app.main; print('SUCCESS: backend.app.main imported')" 2>&1 || echo "FAILED"
cd /app && python3 -c "import app.main; print('SUCCESS: app.main imported')" 2>&1 || echo "FAILED"
