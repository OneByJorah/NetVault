from flask import Blueprint, jsonify, request
from app import db
from app.models import Device, Backup
from app.config import SECRET_KEY
from functools import wraps

bp = Blueprint('restore', __name__, url_prefix='/api/v1/restore')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token or token != SECRET_KEY:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated

@bp.route('/', methods=['POST'])
@token_required
def trigger_restore():
    data = request.get_json()
    commit = data.get('commit')
    target = data.get('target')

    backup = Backup.query.filter_by(version=commit).first_or_404()
    device = Device.query.filter_by(name=target).first_or_404()

    device.config_path = backup.config_file
    db.session.commit()

    return jsonify({
        'message': f'Config {commit} restored to {target}',
        'commit': commit,
        'target': target,
    }), 200

@bp.route('/<string:commit_id>', methods=['GET'])
@token_required
def get_restore(commit_id):
    backup = Backup.query.filter_by(version=commit_id).first_or_404()
    return jsonify({
        'version': backup.version,
        'timestamp': str(backup.timestamp),
        'config_file': backup.config_file,
        'size': backup.size,
        'checksum': backup.checksum,
        'status': backup.status,
        'message': backup.message,
    })
