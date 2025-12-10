from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from supabase_auth import SignUpWithEmailAndPasswordCredentials
from supabase_auth.errors import AuthApiError

from atfirstsight_api.api.api_models.users import UserCredentials, SignupResponse, UserSigninResponse
from atfirstsight_api.api.dependencies.supabase import SupabaseDep

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/signup")
async def signup(creds: UserCredentials, supabase: SupabaseDep) -> UserSigninResponse:
    try:
        auth_response = await supabase.auth.sign_up(
            SignUpWithEmailAndPasswordCredentials(
                email=creds.email,
                password=creds.password
            )
        )
        return UserSigninResponse(**{"id": auth_response.id, **auth_response.session.model_dump()})
    except AuthApiError as e:
        raise HTTPException(status_code=500, detail=f"Failed signup: '{str(e)}'")
