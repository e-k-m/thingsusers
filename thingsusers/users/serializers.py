# TODO: Remove schema naming makes it more light

import marshmallow

from marshmallow import fields


class ViewArgsSchema(marshmallow.Schema):
    id_ = fields.UUID(required=True)

    @marshmallow.post_load
    def post_load(self, data, **kwargs):
        data["id_"] = str(data["id_"])
        return data


class PayloadSchema(marshmallow.Schema):
    id = fields.UUID(dump_only=True)
    email = fields.Email(required=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)

    access_token = fields.Str(dump_only=True, data_key="accessToken")
    refresh_token = fields.Str(dump_only=True, data_key="refreshToken")


class PayloadLoginSchema(marshmallow.Schema):
    email = fields.Email(required=False)
    username = fields.Str(required=False)
    password = fields.Str(required=True, load_only=True)

    @marshmallow.validates_schema
    def validate(self, data, **kwargs):
        if not (data.get("email") or data.get("username")):
            raise marshmallow.ValidationError(
                "Either email or username is required."
            )


class PayloadUpdateSchema(marshmallow.Schema):
    email = fields.Email(required=True)
    username = fields.Str(required=True)
    password = fields.Str(required=False, load_only=True)


view_args_schema = ViewArgsSchema()
payload_schema = PayloadSchema()
payload_login_schema = PayloadLoginSchema()
payload_update_schema = PayloadUpdateSchema()
payloads_schema = PayloadSchema(many=True)
