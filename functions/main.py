"""Cloud Functions (2nd gen) for the SPEED quantum networking platform.

Deployment shape matches the hardware requirements in the project doc:
Python 3.13, 2 vCPU, 1 GiB, 120 s timeout, 1 concurrent request per
instance, 0-3 instances, us-central1.
"""

from firebase_admin import firestore, initialize_app
from firebase_functions import https_fn, options

options.set_global_options(
    region="us-central1",
    memory=options.MemoryOption.GB_1,
    cpu=2,
    timeout_sec=120,
    concurrency=1,
    min_instances=0,
    max_instances=3,
)

initialize_app()


@https_fn.on_call()
def ping(req: https_fn.CallableRequest) -> dict:
    """Smoke test for the callable path and the client's auth wiring.

    Returns the caller's uid when signed in so the frontend can confirm the
    Authentication -> Functions handoff end to end.
    """
    return {
        "ok": True,
        "uid": req.auth.uid if req.auth else None,
    }


@https_fn.on_request()
def api(req: https_fn.Request) -> https_fn.Response:
    """HTTP entry point mounted at /api/** by the Hosting rewrite.

    The simulation engine endpoints will hang off this function; for now it
    only answers a health check so the rewrite can be verified after deploy.
    """
    if req.path.rstrip("/") in ("", "/api", "/api/health", "/health"):
        return https_fn.Response(
            '{"status":"ok"}',
            status=200,
            mimetype="application/json",
        )

    return https_fn.Response(
        '{"error":"not_found"}',
        status=404,
        mimetype="application/json",
    )


@https_fn.on_call()
def create_user_profile(req: https_fn.CallableRequest) -> dict:
    """Create the caller's user document if it does not already exist.

    Written through the Admin SDK so the profile shape stays under server
    control even though the security rules let the owner edit it.
    """
    if req.auth is None:
        raise https_fn.HttpsError(
            code=https_fn.FunctionsErrorCode.UNAUTHENTICATED,
            message="Sign in before creating a profile.",
        )

    db = firestore.client()
    doc_ref = db.collection("users").document(req.auth.uid)

    if doc_ref.get().exists:
        return {"created": False}

    doc_ref.set(
        {
            "ownerId": req.auth.uid,
            "email": req.auth.token.get("email"),
            "displayName": req.auth.token.get("name"),
            "createdAt": firestore.SERVER_TIMESTAMP,
        }
    )
    return {"created": True}
