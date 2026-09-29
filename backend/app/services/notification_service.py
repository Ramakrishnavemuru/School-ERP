from typing import List, Optional
from sqlalchemy.orm import Session
from backend.app.models.notification import Notification
from backend.app.models.user import User

class NotificationService:
    @staticmethod
    def create_notification(
        db: Session,
        user_id: int,
        title: str,
        message: str,
        link: Optional[str] = None,
        notification_type: str = "INFO"
    ) -> Notification:
        notification = Notification(
            user_id=user_id,
            title=title,
            message=message,
            link=link,
            notification_type=notification_type,
            is_read=False
        )
        db.add(notification)
        db.commit()
        db.refresh(notification)
        return notification

    @staticmethod
    def notify_role(
        db: Session,
        role: str,
        title: str,
        message: str,
        link: Optional[str] = None,
        notification_type: str = "INFO"
    ):
        users = db.query(User).filter(User.is_active == True)
        if role != "ALL":
            users = users.filter(User.role == role)
        user_list = users.all()
        for u in user_list:
            db.add(Notification(
                user_id=u.id,
                title=title,
                message=message,
                link=link,
                notification_type=notification_type,
                is_read=False
            ))
        db.commit()

    @staticmethod
    def get_user_notifications(db: Session, user_id: int, unread_only: bool = False, limit: int = 50):
        query = db.query(Notification).filter(Notification.user_id == user_id)
        if unread_only:
            query = query.filter(Notification.is_read == False)
        return query.order_by(Notification.created_at.desc()).limit(limit).all()

    @staticmethod
    def mark_as_read(db: Session, notification_id: int, user_id: int) -> bool:
        n = db.query(Notification).filter(
            Notification.id == notification_id,
            Notification.user_id == user_id
        ).first()
        if n:
            n.is_read = True
            db.commit()
            return True
        return False

    @staticmethod
    def mark_all_as_read(db: Session, user_id: int) -> int:
        count = db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.is_read == False
        ).update({"is_read": True})
        db.commit()
        return count

notification_service = NotificationService()
