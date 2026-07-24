# from sqlalchemy.orm import Session
# from app.models import ActivityLog
# from . import models
# from . import schemas
# from .utils import hash_password
# from .utils import verify_password

# # -------------------------
# # Get User by Email
# # -------------------------

# def get_user_by_email(db: Session, email: str):
#     return (
#         db.query(models.User)
#         .filter(models.User.email == email)
#         .first()
#     )


# # -------------------------
# # Create User
# # -------------------------

# def create_user(db: Session, user: schemas.UserCreate):

#     hashed_pwd = hash_password(user.password)

#     db_user = models.User(
#         full_name=user.full_name,
#         email=user.email,
#         hashed_password=hashed_pwd,
#         role=user.role

#     )

#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)

#     return db_user


# # -------------------------
# # Authenticate User
# # -------------------------

# def authenticate_user(db: Session, email: str, password: str):

#     user = get_user_by_email(db, email)

#     if not user:
#         return None

#     if not verify_password(
#         password,
#         user.hashed_password
#     ):
#         return None

#     return user

# # -------------------------
# # Tasks
# # -------------------------

# def create_task(db: Session, task: schemas.TaskCreate,user_id: int):

#     db_task = models.Task(
#         title=task.title,
#         description=task.description,
#         status=task.status,
#         priority=task.priority,
#         due_date=task.due_date,
#         assigned_to=task.assigned_to,
#         project_id=task.project_id
#     )

#     db.add(db_task)
#     db.commit()
#     db.refresh(db_task)

#     create_activity_log(
#     db=db,
#     user_id=user_id,
#     action="TASK_CREATED",
#     entity_type="Task",
#     entity_id=task.id,
#     description=f"Task '{task.title}' created."
# )
#     create_notification(
#     db=db,
#     user_id=db_task.assigned_to,
#     title="Task Assigned",
#     message=f"You have been assigned task '{db_task.title}'."
# )

#     return db_task

# def get_tasks(
#     db: Session,
#     status: str = None,
#     priority: str = None,
#     assigned_to: int = None
# ):

#     query = db.query(models.Task).filter(
#     models.Task.is_deleted == False
# )

#     if status:
#         query = query.filter(
#             models.Task.status == status
#         )

#     if priority:
#         query = query.filter(
#             models.Task.priority == priority
#         )

#     if assigned_to:
#         query = query.filter(
#             models.Task.assigned_to == assigned_to
#         )

#     return query.all()


# def get_task(db: Session, task_id: int):
#     return db.query(models.Task).filter(
#         models.Task.id == task_id
#     ).first()


# def update_task(
#     db: Session,
#     task_id: int,
#     task: schemas.TaskUpdate
# ):

#     db_task = get_task(db, task_id)
#     if db_task is None:
#         return None

#     update_data = task.model_dump(exclude_unset=True)
#     for key, value in update_data.items():
#         setattr(db_task, key, value)

#     db.commit()
#     db.refresh(db_task)

#     return db_task


# def delete_task(db: Session, task_id: int):
#     db_task = get_task(db, task_id)
#     if db_task is None:
#         return None

#     db_task.is_deleted = True
#     db.commit()

#     return db_task

# # -------------------------
# # Project
# # -------------------------
# def create_project(
#     db: Session,
#     project: schemas.ProjectCreate,
#     user_id: int
# ):

#     db_project = models.Project(
#         name=project.name,
#         description=project.description,
#         created_by=user_id
#     )

#     db.add(db_project)
#     db.commit()
#     db.refresh(db_project)

#     create_activity_log(
#     db=db,
#     user_id=user_id,
#     action="PROJECT_CREATED",
#     entity_type="Project",
#     entity_id=project.id,
#     description=f"Project '{project.name}' created."
#     )
#     return db_project


# def get_projects(
#     db: Session,
#     skip: int = 0,
#     limit: int = 10,
#     search: str = ""
# ):

#     query = db.query(models.Project).filter(
#     models.Project.is_deleted == False
# )

#     if search:
#         query = query.filter(
#             models.Project.name.ilike(f"%{search}%")
#         )
#     return query.offset(skip).limit(limit).all()


# def get_project(db: Session, project_id: int):
#     return db.query(models.Project).filter(
#     models.Project.id == project_id,
#     models.Project.is_deleted == False
# ).first()


# def update_project(
#     db: Session,
#     project_id: int,
#     project: schemas.ProjectCreate,
#     user_id: int
# ):

#     db_project = db.query(models.Project).filter(
#         models.Project.id == project_id
#     ).first()

#     if db_project is None:
#         return None

#     db_project.name = project.name
#     db_project.description = project.description

#     db.commit()
#     db.refresh(db_project)

#     create_activity_log(
#     db=db,
#     user_id=user_id,
#     action="PROJECT_UPDATED",
#     entity_type="Project",
#     entity_id=project.id,
#     description=f"Project '{project.name}' updated."
#     )

#     return db_project


# def delete_project(
#     db: Session,
#     project_id: int,
#     user_id: int
# ):

#     project = db.query(models.Project).filter(
#         models.Project.id == project_id
#     ).first()

#     if project is None:

#         return None

#     project.is_deleted = True
#     db.commit()

#     create_activity_log(
#     db=db,
#     user_id=user_id,
#     action="PROJECT_DELETED",
#     entity_type="Project",
#     entity_id=project.id,
#     description=f"Project '{project.name}' deleted."
# )

#     return project

# # -------------------------
# # Project Member
# # -------------------------

# def add_member(
#     db: Session,
#     project_id: int,
#     user_id: int
# ):

#     member = db.query(models.ProjectMember).filter(
#         models.ProjectMember.project_id == project_id,
#         models.ProjectMember.user_id == user_id
#     ).first()

#     if member:
#         return None

#     new_member = models.ProjectMember(
#         project_id=project_id,
#         user_id=user_id
#     )

#     db.add(new_member)
#     db.commit()
#     db.refresh(new_member)

#     return new_member


# def get_members(
#     db: Session,
#     project_id: int
# ):

#     return db.query(models.ProjectMember).filter(
#         models.ProjectMember.project_id == project_id
#     ).all()


# def remove_member(
#     db: Session,
#     project_id: int,
#     user_id: int
# ):

#     member = db.query(models.ProjectMember).filter(
#         models.ProjectMember.project_id == project_id,
#         models.ProjectMember.user_id == user_id
#     ).first()

#     if member is None:
#         return None

#     db.delete(member)
#     db.commit()

#     return member

# # -------------------------
# # Analytics
# # -------------------------

# def project_summary(
#     db: Session,
#     project_id: int
# ):

#     total = db.query(models.Task).filter(
#         models.Task.project_id == project_id
#     ).count()

#     pending = db.query(models.Task).filter(
#         models.Task.project_id == project_id,
#         models.Task.status == "Pending"
#     ).count()

#     progress = db.query(models.Task).filter(
#         models.Task.project_id == project_id,
#         models.Task.status == "In Progress"
#     ).count()

#     completed = db.query(models.Task).filter(
#         models.Task.project_id == project_id,
#         models.Task.status == "Completed"
#     ).count()

#     return {

#         "total_tasks": total,
#         "pending_tasks": pending,
#         "in_progress_tasks": progress,
#         "completed_tasks": completed

#     }

# # -------------------------
# # Notification
# # -------------------------

# def create_notification(
#     db: Session,
#     user_id: int,
#     title: str,
#     message: str
# ):
#     notification = models.Notification(
#         user_id=user_id,
#         title=title,
#         message=message
#     )

#     db.add(notification)
#     db.commit()
#     db.refresh(notification)

#     return notification

# def get_notifications(db: Session, user_id: int):

#     return (
#         db.query(models.Notification)
#         .filter(models.Notification.user_id == user_id)
#         .order_by(models.Notification.created_at.desc())
#         .all()
#     )

# def get_unread_notifications(db: Session, user_id: int):

#     return (
#         db.query(models.Notification)
#         .filter(
#             models.Notification.user_id == user_id,
#             models.Notification.is_read == False
#         )
#         .all()
#     )   

# def mark_notification_read(
#     db: Session,
#     notification_id: int,
#     user_id: int
# ):

#     notification = (
#         db.query(models.Notification)
#         .filter(
#             models.Notification.id == notification_id,
#             models.Notification.user_id == user_id
#         )
#         .first()
#     )

#     if notification:
#         notification.is_read = True
#         db.commit()
#         db.refresh(notification)

#     return notification

# def mark_all_notifications_read(
#     db: Session,
#     user_id: int
# ):

#     notifications = (
#         db.query(models.Notification)
#         .filter(
#             models.Notification.user_id == user_id,
#             models.Notification.is_read == False
#         )
#         .all()
#     )

#     for notification in notifications:
#         notification.is_read = True

#     db.commit()

#     return notifications

# def delete_notification(
#     db: Session,
#     notification_id: int,
#     user_id: int
# ):

#     notification = (
#         db.query(models.Notification)
#         .filter(
#             models.Notification.id == notification_id,
#             models.Notification.user_id == user_id
#         )
#         .first()
#     )

#     if notification:
#         db.delete(notification)
#         db.commit()

#     return notification
# # -------------------------
# # Activity
# # -------------------------

# def create_activity_log(
#     db: Session,
#     user_id: int,
#     action: str,
#     entity_type: str,
#     entity_id: int,
#     description: str
# ):

#     activity = models.ActivityLog(
#         user_id=user_id,
#         action=action,
#         entity_type=entity_type,
#         entity_id=entity_id,
#         description=description
#     )

#     db.add(activity)
#     db.commit()
#     db.refresh(activity)
#     return activity

# def get_user_activities(
#     db: Session,
#     user_id: int
# ):

#     return (
#         db.query(models.ActivityLog)
#         .filter(models.ActivityLog.user_id == user_id)
#         .order_by(models.ActivityLog.created_at.desc())
#         .all()
#     )

# def get_project_activities(
#     db: Session,
#     project_id: int
# ):

#     return (
#         db.query(models.ActivityLog)
#         .filter(
#             models.ActivityLog.entity_type == "Project",
#             models.ActivityLog.entity_id == project_id
#         )
#         .order_by(models.ActivityLog.created_at.desc())
#         .all()
#     )

# def filter_activity_by_action(
#     db: Session,
#     action: str
# ):

#     return (
#         db.query(models.ActivityLog)
#         .filter(models.ActivityLog.action == action)
#         .all()
#     )

# from datetime import datetime

# def filter_activity_by_date(
#     db: Session,
#     start_date: datetime,
#     end_date: datetime
# ):

#     return (
#         db.query(models.ActivityLog)
#         .filter(
#             models.ActivityLog.created_at >= start_date,
#             models.ActivityLog.created_at <= end_date
#         )
#         .all()
#     )

# # -------------------------
# # Audit Log
# # -------------------------

# def create_audit_log(
#     db: Session,
#     entity_type: str,
#     entity_id: int,
#     field_name: str,
#     old_value: str,
#     new_value: str,
#     changed_by: int
# ):

#     audit = models.AuditLog(
#         entity_type=entity_type,
#         entity_id=entity_id,
#         field_name=field_name,
#         old_value=old_value,
#         new_value=new_value,
#         changed_by=changed_by
#     )

#     db.add(audit)
#     db.commit()
#     db.refresh(audit)
#     return audit

# def get_audit_logs(db: Session):

#     return (
#         db.query(models.AuditLog)
#         .order_by(models.AuditLog.changed_at.desc())
#         .all()
#     )

# def get_audit_logs_by_entity(
#     db: Session,
#     entity_type: str,
#     entity_id: int
# ):

#     return (
#         db.query(models.AuditLog)
#         .filter(
#             models.AuditLog.entity_type == entity_type,
#             models.AuditLog.entity_id == entity_id
#         )
#         .order_by(models.AuditLog.changed_at.desc())
#         .all()
#     )

