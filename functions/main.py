from firebase_functions import https_fn, identity_fn
from firebase_functions.options import set_global_options
from firebase_admin import initialize_app
from firebase_admin import credentials, firestore, auth

# For cost control, you can set the maximum number of containers that can be
# running at the same time. This helps mitigate the impact of unexpected
# traffic spikes by instead downgrading performance. This limit is a per-function
# limit. You can override the limit for each function using the max_instances
# parameter in the decorator, e.g. @https_fn.on_request(max_instances=5).
set_global_options(max_instances=10)

initialize_app()

@https_fn.on_request()
def on_request_example(req: https_fn.Request) -> https_fn.Response:
    
    return https_fn.Response("Hello world!")

@https_fn.on_call(region="us-east1")
def check_invite_token(req: https_fn.CallableRequest) -> dict:

    attempted_token = req.data["token"]
    email = req.data["email"]

    result = {}

    pass #TODO this should receive an invite token and email address, and check if that token is free and available, and if so, attach the email address to the token. It should let the client know whether it succeeded or failed.

    return result

@https_fn.on_call(region="us-east1")
def get_fresh_invite_token(req: https_fn.CallableRequest) -> dict:

    decoded_token = auth.verify_id_token(req.auth.token)
    is_admin = decoded_token.get("admin", False)

    if is_admin == False:
        return "no_token"

    new_token = Invite_Token(Invite_Token.generate_token_text())

    db = firestore.client()

    db.collection("invite_tokens").document(new_token.token).set(new_token.to_dict())

    return new_token.token #TODO There's some polish to apply here, in terms of how the returned text is presented.

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


