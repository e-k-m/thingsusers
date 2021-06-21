import uuid
import datetime

import werkzeug.security
import flask_jwt_extended as jwt


from thingsusers import database

db = database.db


def password_hash(password):
    # NOTE: In real life you would not do 1000 iterations.
    return werkzeug.security.generate_password_hash(
        password, method="pbkdf2:sha256:1000", salt_length=8
    )


def is_valid_password_hash(password_hash, password):
    return werkzeug.security.check_password_hash(password_hash, password)


def create_default_roles_and_permissions():
    role = Role.query.filter(Role.name == "user").first()
    if role:
        return [role]

    permission = Role.query.filter(Role.name == "todocrud").first()
    if not permission:
        permission = Permission("todocrud")
        permission.save()

    role = Role("user")
    role.permissions.append(permission)
    role.save()

    return [role]


rel_user_role = db.Table(
    "rel_user_role",
    db.metadata,
    db.Column("user_id", db.String, db.ForeignKey("user.id"), index=True),
    db.Column("role_id", db.String, db.ForeignKey("role.id"), index=True),
)


rel_role_permission = db.Table(
    "rel_role_permission",
    db.metadata,
    db.Column("role_id", db.String, db.ForeignKey("role.id"), index=True),
    db.Column(
        "permission_id", db.String, db.ForeignKey("permission.id"), index=True
    ),
)


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.String, primary_key=True)
    email = db.Column(db.Text)
    username = db.Column(db.Text)
    password = db.Column(db.Text)

    roles = db.relationship(
        "Role",
        secondary=rel_user_role,
        lazy="dynamic",
        backref=db.backref("users", lazy="dynamic"),
    )

    def __init__(self, email, username, password):
        self.id = str(uuid.uuid4())
        self.email = email
        self.username = username
        self.password = password_hash(password)
        self.roles = create_default_roles_and_permissions()

    def __repr__(self):
        return (
            f"User(id={self.id}, email={self.email}, "
            f"username={self.username}, password={self.password})"
        )

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "roles": self.get_roles(),
            "permissions": self.get_permissions(),
        }

    def payload(self):
        res = self.to_dict()
        res["access_token"] = self.access_token()
        res["refresh_token"] = self.refresh_token()
        return res

    def payload_no_refresh_token(self):
        res = self.to_dict()
        res["access_token"] = self.access_token()
        return res

    def is_valid_password(self, password):
        return is_valid_password_hash(self.password, password)

    def get_roles(self):
        roles = []
        for role in self.roles:
            roles.append(role.to_dict()["name"])
        return roles

    def get_permissions(self):
        permissions = []
        for role in self.roles:
            for permission in role.permissions:
                permissions.append(permission.to_dict()["name"])
        return permissions

    def access_token(self):
        return jwt.create_access_token(
            identity=self.id,
            expires_delta=datetime.timedelta(days=0, seconds=7200),
            user_claims=self.to_dict(),
        )

    def refresh_token(self):
        return jwt.create_refresh_token(identity=self.id)


class Role(db.Model):
    __tablename__ = "role"

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.Text)

    permissions = db.relationship(
        "Permission",
        secondary=rel_role_permission,
        lazy="dynamic",
        backref=db.backref("roles", lazy="dynamic"),
    )

    def __init__(self, name):
        self.id = str(uuid.uuid4())
        self.name = name

    def __repr__(self):
        return f"Role(id={self.id}, name={self.name})"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }


class Permission(db.Model):
    __tablename__ = "permission"

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.Text)

    def __init__(self, name):
        self.id = str(uuid.uuid4())
        self.name = name

    def __repr__(self):
        return f"Permission(id={self.id}, name={self.name})"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }
