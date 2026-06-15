from flask import Blueprint, jsonify, request
from app import db
from app.config import SECRET_KEY, CLOUD_SYNC, RCLONE_CONFIG
from functools import wraps
import subprocess

bp = Blueprint('sync', __name__, url_prefix='/api/v1/sync')

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
def trigger_sync():
    if not CLOUD_SYNC:
        return jsonify({'error': 'Cloud sync is disabled'}), 503

    remote_path = request.get_json().get('remote_path', '/var/lib/netvault/backup')
    cloud_type = request.get_json().get('cloud_type', 's3')
    cloud_path = request.get_json().get('cloud_path', '')

    try:
        # Run rclone sync
        cmd = [
            'rclone',
            'sync',
            f'/var/lib/netvault/backup',
            f'{cloud_type}://{cloud_path}',
            '--progress',
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

        if result.returncode == 0:
            return jsonify({
                'message': 'Cloud sync completed successfully',
                'remote_path': remote_path,
                'cloud_type': cloud_type,
                'cloud_path': cloud_path,
            }), 200
        else:
            return jsonify({
                'error': 'Cloud sync failed',
                'details': result.stderr,
            }), 500

    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Cloud sync timed out'}), 504
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/status', methods=['GET'])
@token_required
def get_sync_status():
    # In production, check rclone status
    return jsonify({
        'status': 'ready',
        'config': RCLONE_CONFIG,
        'cloud_sync': CLOUD_SYNC,
    })
