from firebase_functions import https_fn, identity_fn, options
from firebase_functions.options import set_global_options
from firebase_admin import initialize_app
from firebase_admin import credentials, firestore, auth
from models.invite_token import Invite_Token

# For cost control, you can set the maximum number of containers that can be
# running at the same time. This helps mitigate the impact of unexpected
# traffic spikes by instead downgrading performance. This limit is a per-function
# limit. You can override the limit for each function using the max_instances
# parameter in the decorator, e.g. @https_fn.on_request(max_instances=5).
set_global_options(max_instances=10)

initialize_app()

@https_fn.on_call(region="us-east1")
def delete_user(req: https_fn.CallableRequest) -> dict:

    if req.auth is None:
        raise https_fn.HttpsError(
            code=https_fn.FunctionsErrorCode.UNAUTHENTICATED,
            message="This function must be called by an authenticated user."
        )

    is_admin = req.auth.token.get("admin") is True

    if not is_admin:
        # Raise a PERMISSION_DENIED error if they aren't an admin
        raise https_fn.HttpsError(
            code=https_fn.FunctionsErrorCode.PERMISSION_DENIED,
            message="Access denied. You do not have administrator privileges."
        )

    try:
        email = req.data.get("email")
        if not isinstance(email, str) or not email.strip():
            raise https_fn.HttpsError(
                code=https_fn.FunctionsErrorCode.INVALID_ARGUMENT,
                message="A valid email address is required.",
            )

        user = auth.get_user_by_email(email.strip())
        auth.delete_user(user.uid)

        return {"success": True, "uid": user.uid}
    except auth.UserNotFoundError:
        raise https_fn.HttpsError(
            code=https_fn.FunctionsErrorCode.NOT_FOUND,
            message="No user was found with that email address.",
        )
    except https_fn.HttpsError:
        raise
    except Exception as error:
        print(f"Error deleting user: {error}")
        raise https_fn.HttpsError(
            code=https_fn.FunctionsErrorCode.INTERNAL,
            message="The user could not be deleted.",
        )

@https_fn.on_call(region="us-east1")
def check_invite_token(req: https_fn.CallableRequest) -> dict:

    attempted_token = req.data["token"]
    email = req.data["email"]

    result = {}

    pass #TODO this should receive an invite token and email address, and check if that token is free and available, and if so, attach the email address to the token. It should let the client know whether it succeeded or failed.

    return result

@https_fn.on_call(region="us-east1")
def get_fresh_invite_tokenv2(req: https_fn.CallableRequest) -> dict:

    if req.auth is None:
        raise https_fn.HttpsError(
            code=https_fn.FunctionsErrorCode.UNAUTHENTICATED,
            message="This function must be called by an authenticated user."
        )

    is_admin = req.auth.token.get("admin") is True

    if not is_admin:
        # Raise a PERMISSION_DENIED error if they aren't an admin
        raise https_fn.HttpsError(
            code=https_fn.FunctionsErrorCode.PERMISSION_DENIED,
            message="Access denied. You do not have administrator privileges."
        )
    else:
        new_token = Invite_Token(Invite_Token.generate_token_text())

        db = firestore.client()

        db.collection("invite_tokens").document(new_token.token).set(new_token.to_dict())

        return {"invite-token": new_token.token, "expires": new_token.expires.isoformat()}

##This tells how to complete this on the user side: https://firebase.google.com/docs/auth/extend-with-blocking-functions#blocking_registration_or_sign-in
@identity_fn.before_user_created()
def check_new_user_for_invite(
    event: identity_fn.AuthBlockingEvent,
) -> identity_fn.BeforeCreateResponse | None:

    user = event.data
    email = user.email

    ##Get the invite token, see if it's legit ... if not, do the error below TODO
    raise https_fn.HttpsError(
    code=https_fn.FunctionsErrorCode.PERMISSION_DENIED,
    message="Invite not valid!")


