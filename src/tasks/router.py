from fastapi import APIRouter, Depends

from auth.auth import current_user
from tasks.tasks import my_first_task

router = APIRouter(prefix="/send_email_msg")


@router.get("/send_me_msg")
def get_dashboard_report(user=Depends(current_user)):
    my_first_task.delay(username=user.username, email_address=user.email)
    return {
        "Status": 200,
        "data": "Письмо отправлено",
        "details": None
    }
