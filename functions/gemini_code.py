from firebase_functions import https_fn

@https_fn.on_call()
def get_user_profile(req: https_fn.CallableRequest) -> dict:
    # 1. Verify the user is authenticated
    if req.auth is None:
        raise https_fn.HttpsError(
            code=https_fn.FunctionsErrorCode.UNAUTHENTICATED,
            message="This function must be called by an authenticated user."
        )
    
    # 2. Check for the 'admin' custom claim
    # Safely fetches 'admin' and ensures it is explicitly True
    is_admin = req.auth.token.get("admin") is True
    
    if not is_admin:
        # Raise a PERMISSION_DENIED error if they aren't an admin
        raise https_fn.HttpsError(
            code=https_fn.FunctionsErrorCode.PERMISSION_DENIED,
            message="Access denied. You do not have administrator privileges."
        )
    
    # 3. User is an admin, proceed with the administrative logic
    uid = req.auth.uid
    email = req.auth.token.get("email")
    
    return {
        "status": "success",
        "message": "Welcome to the Admin Dashboard!",
        "uid": uid,
        "email": email,
        "is_admin": is_admin
    }
