# CSHSSO API documentation
All API requests, if not specified otherwise, require authentication.
The authentication is performed via a session ID and a session secret.
Both data is provided via respective Cookies, namely `cshsso-session-id`
and `cshsso-session-secret` respectively.
Both must be sent by the client on each request that requres authentication.

## Login
Does not require authentication, duh!  
`POST` `/login`
`Content-Type: application/json`
```JSON
{
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "Login request",
    "description": "Log a user in",
    "type": "object",
    "properties": {
        "email": {
            "description": "The email address of the user who wants to log in",
            "type": "string"
        },
        "passwd": {
            "description": "The password of the user who wants to log in",
            "type": "string"
        }
    },
    "required": ["email", "passwd"]
}
```

## Logout
`POST` `/logout`
`Content-Type: application/json`
```JSON
{
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "Logout request",
    "description": "Logout a user",
    "type": "object",
    "properties": {
        "all": {
            "description": "Flag, whether all sessions of the user shall be terminated",
            "type": "boolean"
        }
    },
    "required": []
}
```

## Password reset
To reset a password, the user must first request a password reset.
After that, they get an email containing a reset link.
The reset link, contains a reset token, that must be passed to 
the actual password reset endpoint.

### Request reset link
`POST` `/pwreset`
`Content-Type: application/json`
```JSON
{
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "Password reset link request",
    "description": "Request a password reset link",
    "type": "object",
    "properties": {
        "email": {
            "description": "The email address of the user account",
            "type": "string"
        }
    },
    "required": ["email"]
}
```

### Perform password reset
`POST` `/pwreset/confirm`
`Content-Type: application/json`
```JSON
{
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "Password reset request",
    "description": "Perform actual password reset",
    "type": "object",
    "properties": {
        "token": {
            "description": "The password reset token from the email",
            "type": "string"
        },
        "passwd": {
            "description": "The new password for the user account",
            "type": "string"
        }
    },
    "required": ["token", "passwd"]
}
```

## Registration
To register new users, anybody can registern themselves via an
unauthorized request.
A valid recaptcha response must be provided to register to avoid spam.
In order to be able to use the new user account, a Charge must confirm
the new user.

### Register a new user
No authentication, but a ReCAPTCHA response is required!  
`POST` `/register`
`Content-Type: application/json`
```JSON
{
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "New user",
    "description": "Register a new user",
    "type": "object",
    "properties": {
        "response": {
            "description": "The ReCAPTCHA response",
            "type": "string"
        },
        "email": {
            "description": "The user's email address",
            "type": "string"
        },
        "passwd": {
            "description": "The user's password",
            "type": "string"
        },
        "first_name": {
            "description": "The user's first name",
            "type": "string"
        },
        "last_name": {
            "description": "The user's last name",
            "type": "string"
        },
        "status": {
            "description": "The user's status",
            "type": "string"
        }
    },
    "required": ["response", "email", "passwd", "first_name", "last_name", "status"]
}
```

### Confirm a new user
Authorized groups: `CHARGES`  
`POST` `/register/confirm`
`Content-Type: application/json`
```JSON
{
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "Confirm user",
    "description": "Confirm a new user",
    "type": "object",
    "properties": {
        "user": {
            "description": "The user's ID",
            "type": "integer"
        }
    },
    "required": ["user"]
}
```

## Show account data
`GET` `/account`
`Accept: application/json`
### User view
```JSON
{
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "New user",
    "description": "Register a new user",
    "type": "object",
    "properties": {
        "id": {
            "description": "The user's ID",
            "type": "integer"
        },
        "email": {
            "description": "The user's email address",
            "type": "string"
        },
        "passwd": {
            "description": "The user's password",
            "type": "string"
        },
        "first_name": {
            "description": "The user's first name",
            "type": "string"
        },
        "last_name": {
            "description": "The user's last name",
            "type": "string"
        },
        "status": {
            "description": "The user's status",
            "type": "string"
        },
        "registered": {
            "description": "The user's registration date",
            "type": "string"
        },
        "acception": {
            "description": "The user's acception date",
            "type": "string"
        },
        "reception": {
            "description": "The user's reception date",
            "type": "string"
        },
        "commissions": {"type": "array",
            "items": {
                "type": "object"
            },
            "minItems": 0,
            "uniqueItems": true
        }
    },
    "required": ["id", "email", "passwd", "first_name", "last_name", "status", "registered", "commissions"]
}
```
### Admin view
An admin can *additionally* see the following fields:
```JSON
{
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "New user",
    "description": "Register a new user",
    "type": "object",
    "properties": {
        "verified": {
            "description": "Flag whether the user has been verified",
            "type": "boolean"
        },
        "locked": {
            "description": "Flag whether the user has been locked",
            "type": "boolean"
        },
        "failed_logins": {
            "description": "Amount of failed logins",
            "type": "integer"
        },
        "admin": {
            "description": "Flag whether the user is an admin",
            "type": "boolean"
        }
    },
    "required": ["verified", "locked", "failed_logins", "admin"]
}
```

## Modify account data
TODO...
