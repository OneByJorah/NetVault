from flask import Blueprint, jsonify, request
from app import db
from app.models import Device, Backup
from app.config import SECRET_KEY
from functools import wraps

bp = Blueprint('devices', __name__, url_prefix='/api/v1/devices')

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
def list_devices():
    devices = Device.query.all()
    return jsonify([{
        'id': d.id,
        'name': d.name,
        'hostname': d.hostname,
        'ip_address': d.ip_address,
        'os_type': d.os_type,
        'username': d.username,
        'protocol': d.protocol,
        'port': d.port,
        'enabled': d.enabled,
        'last_backup': str(d.last_backup) if d.last_backup else None,
        'backup_count': d.backup_count,
    } for d in devices])

@bp.route('/<int:device_id>', methods=['GET'])
@token_required
def get_device(device_id):
    device = Device.query.get_or_404(device_id)
    return jsonify({
        'id': device.id,
        'name': device.name,
        'hostname': device.hostname,
        'ip_address': device.ip_address,
        'os_type': device.os_type,
        'username': device.username,
        'password': device.password,
        'protocol': device.protocol,
        'port': device.port,
        'enabled': device.enabled,
        'last_backup': str(device.last_backup) if device.last_backup else None,
        'backup_count': device.backup_count,
    })

@bp.route('/<int:device_id>', methods=['PUT'])
@token_required
def update_device(device_id):
    device = Device.query.get_or_404(device_id)
    data = request.get_json()

    if 'hostname' in data:
        device.hostname = data['hostname']
    if 'ip_address' in data:
        device.ip_address = data['ip_address']
    if 'os_type' in data:
        device.os_type = data['os_type']
    if 'username' in data:
        device.username = data['username']
    if 'password' in data:
        device.password = data['password']
    if 'protocol' in data:
        device.protocol = data['protocol']
    if 'port' in data:
        device.port = data['port']
    if 'enabled' in data:
        device.enabled = data['enabled']

    db.session.commit()
    return jsonify({'message': 'Device updated'}), 200

@bp.route('/<int:device_id>', methods=['DELETE'])
@token_required
def delete_device(device_id):
    device = Device.query.get_or_404(device_id)
    db.session.delete(device)
    db.session.commit()
    return jsonify({'message': 'Device deleted'}), 200

@bp.route('/<int:device_id>/backup', methods=['POST'])
@token_required
def backup_device(device_id):
    device = Device.query.get_or_404(device_id)
    device.backup_count += 1
    db.session.commit()
    return jsonify({'message': f'Backup initiated for {device.name}'}), 200
