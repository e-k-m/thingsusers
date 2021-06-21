from wtoolzexceptions import exceptions
import flask
import flask_jwt_extended as jwt

from thingsusers.users import models as users_models
from thingsusers.users import serializers as users_serializers
from thingsusers import utils

blueprint = flask.Blueprint("users", __name__)


@blueprint.route("/api/v0.0/users/register", methods=("POST",))
def register_user():
    payload = utils.parse(users_serializers.payload_schema, "json")

    r = users_models.User.query.filter(
        users_models.User.email == payload["email"]
    ).first()

    if r:
        exceptions.ohoh(400, "email already taken.")

    res = users_models.User(**payload)
    res.save()

    return (
        users_serializers.payload_schema.dump(res.payload()),
        201,
    )


@blueprint.route("/api/v0.0/users/login", methods=("POST",))
def login_user():
    payload = utils.parse(users_serializers.payload_login_schema, "json")

    if "email" in payload:
        res = users_models.User.query.filter(
            users_models.User.email == payload["email"]
        ).first()
        if not res:
            exceptions.ohoh(404)

    elif "username" in payload:
        res = users_models.User.query.filter(
            users_models.User.username == payload["username"]
        ).first()
        if not res:
            exceptions.ohoh(404)

    is_valid_password = res.is_valid_password(payload["password"])
    if not is_valid_password:
        raise exceptions.ohoh(409, "Username, email or password invalid.")

    else:
        return (
            users_serializers.payload_schema.dump(res.payload()),
            201,
        )


@blueprint.route("/api/v0.0/users/info", methods=("GET",))
@jwt.jwt_required
def info_user():
    res = users_models.User.query.get(jwt.get_jwt_identity())
    if not res:
        exceptions.ohoh(404)

    return (
        users_serializers.payload_schema.dump(res.to_dict()),
        200,
    )


@blueprint.route("/api/v0.0/users/refresh", methods=("GET",))
@jwt.jwt_refresh_token_required
def refresh_user():
    res = users_models.User.query.get(jwt.get_jwt_identity())
    if not res:
        # TODO: Review this error code, maybe 422
        exceptions.ohoh(404)

    return (
        users_serializers.payload_schema.dump(res.payload_no_refresh_token()),
        201,
    )


@blueprint.route("/api/v0.0/users/<id_>", methods=("PUT",))
@jwt.jwt_required
def update_user(id_):
    args = utils.parse(users_serializers.view_args_schema, "view_args")
    if jwt.get_jwt_identity() != args["id_"]:
        exceptions.ohoh(403)

    res = users_models.User.query.get(args["id_"])
    if not res:
        exceptions.ohoh(404)

    payload = utils.parse(users_serializers.payload_update_schema, "json")

    res.update(**payload)
    res.save()

    return users_serializers.payload_schema.dump(res.to_dict()), 201


@blueprint.route("/api/v0.0/users/<id_>", methods=("DELETE",))
@jwt.jwt_required
def delete_user(id_):
    args = utils.parse(users_serializers.view_args_schema, "view_args")
    if jwt.get_jwt_identity() != args["id_"]:
        exceptions.ohoh(403)

    res = users_models.User.query.get(args["id_"])
    if not res:
        exceptions.ohoh(404)

    res.delete()

    return "", 204
