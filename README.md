# thingsusers

![](https://github.com/e-k-m/thingsusers/workflows/main/badge.svg)

> service for managing users

[Installation and Usage](#installation-and-usage) | [Environment Variables](#environment-variables) | [Getting Up And Running](#getting-up-and-running) | [API](#api) | [Benchmarks](#benchmarks) | [See Also](#see-also)

The main feature are:

- Manages users

## Installation and Usage

```bash
pip install .
# set env var
thingsusers-utils db upgrade
<your favorite wsgi server> thingsusers:app
```

## Environment Variables

- THINGS_USERS_DATABASE: SQLAlchemy database connection URL e.g.
postgresql://postgres:mysecretpassword@localhost/thingsusers or
sqlite:///todo.db.

- THINGS_USERS_SECRET: A secret.

- THINGS_USERS_LOG_LEVEL: Log level to be used, defaults to
WARNING. Possible values are DEBUG INFO WARNING ERROR, CRITICAL or
NOTSET.

## Getting Up and Running

```bash
nox -l
```

## API

```yml 
# FIXME: Review some stuff is not documented.
openapi: 3.0.0
info:
  title: Users API
  description: Service for managing users
  version: 0.0.0.dev
servers:
  - url: "https://users.infra3d.ch/api/v0.0"
    description: Production server
  - url: "https://users.devel.infra3d.ch/api/v0.0"
    description: Development server
paths:
  /users/register:
    post:
      summary: Register User
      requestBody:
        description: User
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/User'
      responses:
        '201':
          description: UserContext
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/UserContext"
        default:
          description: Unexpected error
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"
  /users/login:
    post:
      summary: Login User
      requestBody:
        description: User given by username or email and password
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/User'
      responses:
        '201':
          description: UserContext
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/UserContext"
        default:
          description: Unexpected error
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"
  /users/info:
    get:
      summary: Get User Info
      responses:
        '200':
          description: UserInfoContext
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/UserInfoContext"
        default:
          description: Unexpected error
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"
  /users/refresh:
    get:
      summary: Refresh UserContext
      responses:
        '201':
          description: UserRefreshContext 
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/UserRefreshContext"
        default:
          description: Unexpected error
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"
  /users/{id}:
    put:
      summary: Update User
      parameters:
        - name: id
          in: path
          required: true
          description: User ID
          schema:
            type: string
      requestBody:
        description: UpdateUser
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UpdateUser'
      responses:
        '201':
          description: UserInfoContext
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/UserInfoContext"
        default:
          description: Unexpected error
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"
    delete:
      summary: Delete User
      parameters:
        - name: id
          in: path
          required: true
          description: User ID
          schema:
            type: string
      responses:
        '204':
          description: Null response
        default:
          description: Unexpected error
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"                                
components:
  schemas:
    User:
      type: object
      required:
        - email
        - username
        - password
      properties:
        email:
          type: string
          format: email
        username:
          type: string
        password:
          type: string
    UpdateUser:
      type: object
      required:
        - email
        - username
      properties:
        email:
          type: string
          format: email
        username:
          type: string
        password:
          type: string
    UserContext:
      type: object
      properties:
        id:
          type: string
        email:
          type: string
          format: email
        username:
          type: string
        accessToken:
          type: string
        refreshToken:
          type: string         
    UserInfoContext:
      type: object
      properties:
        id:
          type: string
        email:
          type: string
          format: email
        username:
          type: string
    UserRefreshContext:
      type: object
      properties:
        id:
          type: string
        email:
          type: string
          format: email
        username:
          type: string
        accessToken:
          type: string          
    ErrorResponse:
      type: object
      required:
        - error
      properties:
        error:
          $ref: "#/components/schemas/Error"
    Error:
      type: object
      required:
        - code
        - message
      properties:
        code:
          type: string
        message:
          type: string
        target:
          type: string
        details:
          type: array
          items:
            $ref: "#/components/schemas/Error"
        innererror:
          $ref: "#/components/schemas/InnerError"
    InnerError:
      type: object
      additionalProperties: true
      properties:
        code:
          type: string
        innererror:
          $ref: "#/components/schemas/InnerError"

```

## Benchmarks

```text
FIXME
```

## See Also

- [things](https://github.com/e-k-m/things): A frontend using this service.

- [thingstodo](https://github.com/e-k-m/thingstodo): A service that runs in conjuction with this service.

- [wtoolzargs](https://github.com/e-k-m/wtoolzargs) and [wtoolzexceptions](https://github.com/e-k-m/wtoolzexceptions): Libraries used
  in this service.