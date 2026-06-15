from flask import Blueprint

devices_bp = Blueprint('devices', __name__, url_prefix='/api/v1/devices')
backup_bp = Blueprint('backup', __name__, url_prefix='/api/v1/backup')
restore_bp = Blueprint('restore', __name__, url_prefix='/api/v1/restore')
compare_bp = Blueprint('compare', __name__, url_prefix='/api/v1/compare')
alerts_bp = Blueprint('alerts', __name__, url_prefix='/api/v1/alerts')
sync_bp = Blueprint('sync', __name__, url_prefix='/api/v1/sync')
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')
