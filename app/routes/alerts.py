from flask import Blueprint, jsonify, request
from app import db
from app.models import Device, Alert
from app.config import SECRET_KEY
from datetime import datetime
from functools import wraps

bp = Blueprint('alerts', __name__, url_prefix='/api/v1/alerts')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token or token != SECRET_KEY:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated

@bp.route('/', methods=['GET'])
@token_required
def list_alerts():
    alerts = Alert.query.order_by(Alert.timestamp.desc()).all()
    return jsonify([{
        'id': a.id,
        'device_id': a.device_id,
        'type': a.type,
        'level': a.level,
        'message': a.message,
        'timestamp': str(a.timestamp),
        'resolved': a.resolved,
        'webhook': a.webhook,
    } for a in alerts])

@bp.route('/<int:alert_id>', methods=['GET'])
@token_required
def get_alert(alert_id):
    alert = Alert.query.get_or_404(alert_id)
    return jsonify({
        'id': alert.id,
        'device_id': alert.device_id,
        'type': alert.type,
        'level': alert.level,
        'message': alert.message,
        'timestamp': str(alert.timestamp),
        'resolved': alert.resolved,
        'webhook': alert.webhook,
    })

@bp.route('/', methods=['POST'])
@token_required
def create_alert():
    data = request.get_json()
    device_id = data.get('device_id')
    alert_type = data.get('type', 'info')
    level = data.get('level', 'info')
    message = data.get('message')
    webhook = data.get('webhook', '')

    alert = Alert(
        device_id=device_id,
        type=alert_type,
        level=level,
        message=message,
        timestamp=datetime.now(),
        webhook=webhook,
    )
    db.session.add(alert)
    db.session.commit()

    return jsonify({
        'message': 'Alert created',
        'id': alert.id,
        'type': alert_type,
        'level': level,
        'message': message,
    }), 201

@bp.route('/<int:alert_id>', methods=['DELETE'])
@token_required
def resolve_alert(alert_id):
    alert = Alert.query.get_or_404(alert_id)
    alert.resolved = True
    db.session.commit()
    return jsonify({'message': 'Alert resolved'}), 200
