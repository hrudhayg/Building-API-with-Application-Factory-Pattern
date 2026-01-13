cat > flask_app.py <<'EOF'
import os
from project.application import create_app

env = os.getenv("FLASK_ENV", "production").lower()

if env == "testing":
    app = create_app("TestingConfig")
elif env == "development":
    app = create_app("DevelopmentConfig")
else:
    app = create_app("ProductionConfig")
EOF
