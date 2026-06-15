import os

def create_app():
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    from flask_migrate import Migrate
    from flask_cors import CORS

    db = SQLAlchemy()
    migrate = Migrate()
    CORS()

    app = Flask(__name__)

    # Load config
    config_file = os.path.join(os.path.dirname(__file__), '..', 'config', 'default.conf')
    if os.path.exists(config_file):
        import yaml
        with open(config_file) as f:
            config = yaml.safe_load(f)
    else:
        config = {
            'SERVER_NAME': 'netvault.local',
            'SECRET_KEY': 'dev-secret-key',
            'DATABASE_URL': 'sqlite:///netvault.db',
            'FTP_ENABLED': True,
            'SFTP_ENABLED': True,
            'TFTP_ENABLED': True,
            'OXIDIZED_ENABLED': True,
            'GIT_ENABLED': True,
            'CLOUD_SYNC': False,
        }

    app.config.update({
        'SECRET_KEY': config.get('SECRET_KEY', 'dev-secret-key'),
        'DATABASE_URL': config.get('DATABASE_URL', 'sqlite:///netvault.db'),
        'SERVER_NAME': config.get('SERVER_NAME', 'netvault.local'),
    })

    db.init_app(app)
    migrate.init_app(app)

    # Import routes
    from app.routes import devices, backup, restore, compare, alerts, sync, api
    app.register_blueprint(devices.bp)
    app.register_blueprint(backup.bp)
    app.register_blueprint(restore.bp)
    app.register_blueprint(compare.bp)
    app.register_blueprint(alerts.bp)
    app.register_blueprint(sync.bp)
    app.register_blueprint(api.bp)

    @app.route('/')
    def index():
        from flask import redirect
        return redirect('/dashboard')

    return app
