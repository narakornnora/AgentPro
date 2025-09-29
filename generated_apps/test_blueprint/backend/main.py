from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import models, schemas

DATABASE_URL = "sqlite:///./app.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI(title="AI Blueprint API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def on_startup():
    models.Base.metadata.create_all(bind=engine)

@app.get('/health')
def health():
    return {"status":"ok"}

# CRUD for Posts
@app.get("/api/posts")
def list_posts(db: Session = Depends(get_db)):
    return db.query(models.Posts).all()

@app.post("/api/posts")
def create_posts(item: schemas.PostsIn, db: Session = Depends(get_db)):
    obj = models.Posts(**item.model_dump(exclude_unset=True))
    db.add(obj); db.commit(); db.refresh(obj); return obj

@app.get("/api/posts/{item_id}")
def get_posts(item_id: int, db: Session = Depends(get_db)):
    return db.query(models.Posts).get(item_id)

@app.put("/api/posts/{item_id}")
def update_posts(item_id: int, item: schemas.PostsIn, db: Session = Depends(get_db)):
    obj = db.query(models.Posts).get(item_id)
    if not obj: return {"error":"not found"}
    for k,v in item.model_dump(exclude_unset=True).items(): setattr(obj,k,v)
    db.commit(); db.refresh(obj); return obj

@app.delete("/api/posts/{item_id}")
def delete_posts(item_id: int, db: Session = Depends(get_db)):
    obj = db.query(models.Posts).get(item_id)
    if not obj: return {"ok": False}
    db.delete(obj); db.commit(); return {"ok": True}

# CRUD for Users
@app.get("/api/users")
def list_users(db: Session = Depends(get_db)):
    return db.query(models.Users).all()

@app.post("/api/users")
def create_users(item: schemas.UsersIn, db: Session = Depends(get_db)):
    obj = models.Users(**item.model_dump(exclude_unset=True))
    db.add(obj); db.commit(); db.refresh(obj); return obj

@app.get("/api/users/{item_id}")
def get_users(item_id: int, db: Session = Depends(get_db)):
    return db.query(models.Users).get(item_id)

@app.put("/api/users/{item_id}")
def update_users(item_id: int, item: schemas.UsersIn, db: Session = Depends(get_db)):
    obj = db.query(models.Users).get(item_id)
    if not obj: return {"error":"not found"}
    for k,v in item.model_dump(exclude_unset=True).items(): setattr(obj,k,v)
    db.commit(); db.refresh(obj); return obj

@app.delete("/api/users/{item_id}")
def delete_users(item_id: int, db: Session = Depends(get_db)):
    obj = db.query(models.Users).get(item_id)
    if not obj: return {"ok": False}
    db.delete(obj); db.commit(); return {"ok": True}

# CRUD for Notifications
@app.get("/api/notifications")
def list_notifications(db: Session = Depends(get_db)):
    return db.query(models.Notifications).all()

@app.post("/api/notifications")
def create_notifications(item: schemas.NotificationsIn, db: Session = Depends(get_db)):
    obj = models.Notifications(**item.model_dump(exclude_unset=True))
    db.add(obj); db.commit(); db.refresh(obj); return obj

@app.get("/api/notifications/{item_id}")
def get_notifications(item_id: int, db: Session = Depends(get_db)):
    return db.query(models.Notifications).get(item_id)

@app.put("/api/notifications/{item_id}")
def update_notifications(item_id: int, item: schemas.NotificationsIn, db: Session = Depends(get_db)):
    obj = db.query(models.Notifications).get(item_id)
    if not obj: return {"error":"not found"}
    for k,v in item.model_dump(exclude_unset=True).items(): setattr(obj,k,v)
    db.commit(); db.refresh(obj); return obj

@app.delete("/api/notifications/{item_id}")
def delete_notifications(item_id: int, db: Session = Depends(get_db)):
    obj = db.query(models.Notifications).get(item_id)
    if not obj: return {"ok": False}
    db.delete(obj); db.commit(); return {"ok": True}

# CRUD for Messages
@app.get("/api/messages")
def list_messages(db: Session = Depends(get_db)):
    return db.query(models.Messages).all()

@app.post("/api/messages")
def create_messages(item: schemas.MessagesIn, db: Session = Depends(get_db)):
    obj = models.Messages(**item.model_dump(exclude_unset=True))
    db.add(obj); db.commit(); db.refresh(obj); return obj

@app.get("/api/messages/{item_id}")
def get_messages(item_id: int, db: Session = Depends(get_db)):
    return db.query(models.Messages).get(item_id)

@app.put("/api/messages/{item_id}")
def update_messages(item_id: int, item: schemas.MessagesIn, db: Session = Depends(get_db)):
    obj = db.query(models.Messages).get(item_id)
    if not obj: return {"error":"not found"}
    for k,v in item.model_dump(exclude_unset=True).items(): setattr(obj,k,v)
    db.commit(); db.refresh(obj); return obj

@app.delete("/api/messages/{item_id}")
def delete_messages(item_id: int, db: Session = Depends(get_db)):
    obj = db.query(models.Messages).get(item_id)
    if not obj: return {"ok": False}
    db.delete(obj); db.commit(); return {"ok": True}
