from app import db

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    hostname = db.Column(db.String(128))
    ip_address = db.Column(db.String(46))
    os_type = db.Column(db.String(64))
    username = db.Column(db.String(64))
    password = db.Column(db.String(128))
    protocol = db.Column(db.String(8), default='ssh')
    port = db.Column(db.Integer, default=22)
    enabled = db.Column(db.Boolean, default=True)
    last_backup = db.Column(db.DateTime)
    backup_count = db.Column(db.Integer, default=0)

    backups = db.relationship('Backup', backref='device', lazy=True)

    def __repr__(self):
        return f'<Device {self.name}>'

class Backup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
    version = db.Column(db.String(64), unique=True)
    timestamp = db.Column(db.DateTime)
    config_file = db.Column(db.String(512))
    size = db.Column(db.Integer)
    checksum = db.Column(db.String(64))
    status = db.Column(db.String(8), default='completed')
    message = db.Column(db.String(256))

    def __repr__(self):
        return f'<Backup {self.device_id}/{self.version}>'

class Commit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hash = db.Column(db.String(40), unique=True)
    message = db.Column(db.String(256))
    author = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime)
    branch = db.Column(db.String(32), default='main')

    devices = db.relationship('DeviceCommit', backref='commit', lazy=True)

class DeviceCommit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
    commit_id = db.Column(db.Integer, db.ForeignKey('commit.id'), nullable=False)
    file = db.Column(db.String(512))
    line = db.Column(db.Integer)
    added = db.Column(db.Integer, default=0)
    removed = db.Column(db.Integer, default=0)
    changed = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<DeviceCommit {self.device_id}/{self.commit_id}>'

class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'))
    type = db.Column(db.String(32))
    level = db.Column(db.String(8), default='info')
    message = db.Column(db.String(512))
    timestamp = db.Column(db.DateTime)
    resolved = db.Column(db.Boolean, default=False)
    webhook = db.Column(db.String(256))

    def __repr__(self):
        return f'<Alert {self.id}>'
