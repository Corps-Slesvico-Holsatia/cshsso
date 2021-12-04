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
    "email": <str:email_address>,
    "passwd": <str:password>
}
```

## Logout
`POST` `/logout`
`Content-Type: application/json`
```JSON
{
    "all": <bool:terminate_all_sessions>
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
    "email": <str:email_address>
}
```

### Perform password reset
`POST` `/pwreset/confirm`
`Content-Type: application/json`
```JSON
{
    "token": <str:password_reset_token>,
    "passwd": <str:new_password>
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
    "response": <str:recaptcha_response>,
    "email": <str:email_address>,
    "passwd": <str:password>,
    "first_name": <str:first_name>,
    "last_name": <str:last_name>,
    "status": <str:status>
}
```

### Confirm a new user
Authorized groups: `CHARGES`  
`POST` `/register/confirm`
`Content-Type: application/json`
```JSON
{
    "user": <int:user_id>
}
```

## Show account data
`GET` `/account`
`Accept: application/json`
### User view
```JSON
{
    "id": <int:user_id>,
    "email": <str:email_address>,
    "first_name": <str:first_name>,
    "last_name": <str:last_name>,
    "status": <JSON:status>,
    "registered": <str:registration_date>,
    "acception": <str|null:acception_date>,
    "reception": <str|null:reception_date>,
    "commissions": [
        <JSON:commission>,
        ...
    ]
}
```
### Admin view
An admin can *additionally* see the following fields:
```JSON
{
    "verified": <bool:user_is_verified>,
    "locked": <bool:user_is_locked>,
    "failed_logins": <int:amount_of_failed_logins>,
    "admin": <bool:user_is_admin>
}
```

## Modify account data
TODO...
