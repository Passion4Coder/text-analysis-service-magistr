from fastapi import APIRouter, HTTPException, Depends, Header
from app.admin.service import clear_database
from app.core.config import settings

router = APIRouter(prefix="/admin", tags=["Адмін панель 🔧"])


async def verify_admin(x_admin_key: str = Header(...)):
    if x_admin_key != settings.ADMIN_SECRET:
        raise HTTPException(status_code=403, detail="Не авторизовано")


@router.delete(
    "/reset-db", dependencies=[Depends(verify_admin)], summary="Очистити всю базу даних"
)
async def reset_database(admin: None = Depends(verify_admin)):
    return await clear_database()
