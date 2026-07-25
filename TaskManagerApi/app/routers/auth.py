from ..dependencies import get_current_user
from ..models import User

@router.get("/me", response_model=schemas.UserResponse)
def get_me(
    current_user: User = Depends(get_current_user)
):
    return current_user