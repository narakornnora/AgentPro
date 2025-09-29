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

# CRUD for Coffee
@app.get("/api/coffees")
def list_coffees(db: Session = Depends(get_db)):
    return db.query(models.Coffee).all()

@app.post("/api/coffees")
def create_coffee(item: schemas.CoffeeIn, db: Session = Depends(get_db)):
    obj = models.Coffee(**item.model_dump(exclude_unset=True))
    db.add(obj); db.commit(); db.refresh(obj); return obj

@app.get("/api/coffees/{item_id}")
def get_coffee(item_id: int, db: Session = Depends(get_db)):
    return db.query(models.Coffee).get(item_id)

@app.put("/api/coffees/{item_id}")
def update_coffee(item_id: int, item: schemas.CoffeeIn, db: Session = Depends(get_db)):
    obj = db.query(models.Coffee).get(item_id)
    if not obj: return {"error":"not found"}
    for k,v in item.model_dump(exclude_unset=True).items(): setattr(obj,k,v)
    db.commit(); db.refresh(obj); return obj

@app.delete("/api/coffees/{item_id}")
def delete_coffee(item_id: int, db: Session = Depends(get_db)):
    obj = db.query(models.Coffee).get(item_id)
    if not obj: return {"ok": False}
    db.delete(obj); db.commit(); return {"ok": True}

# CRUD for Order
@app.get("/api/orders")
def list_orders(db: Session = Depends(get_db)):
    return db.query(models.Order).all()

@app.post("/api/orders")
def create_order(item: schemas.OrderIn, db: Session = Depends(get_db)):
    obj = models.Order(**item.model_dump(exclude_unset=True))
    db.add(obj); db.commit(); db.refresh(obj); return obj

@app.get("/api/orders/{item_id}")
def get_order(item_id: int, db: Session = Depends(get_db)):
    return db.query(models.Order).get(item_id)

@app.put("/api/orders/{item_id}")
def update_order(item_id: int, item: schemas.OrderIn, db: Session = Depends(get_db)):
    obj = db.query(models.Order).get(item_id)
    if not obj: return {"error":"not found"}
    for k,v in item.model_dump(exclude_unset=True).items(): setattr(obj,k,v)
    db.commit(); db.refresh(obj); return obj

@app.delete("/api/orders/{item_id}")
def delete_order(item_id: int, db: Session = Depends(get_db)):
    obj = db.query(models.Order).get(item_id)
    if not obj: return {"ok": False}
    db.delete(obj); db.commit(); return {"ok": True}

# CRUD for Location
@app.get("/api/locations")
def list_locations(db: Session = Depends(get_db)):
    return db.query(models.Location).all()

@app.post("/api/locations")
def create_location(item: schemas.LocationIn, db: Session = Depends(get_db)):
    obj = models.Location(**item.model_dump(exclude_unset=True))
    db.add(obj); db.commit(); db.refresh(obj); return obj

@app.get("/api/locations/{item_id}")
def get_location(item_id: int, db: Session = Depends(get_db)):
    return db.query(models.Location).get(item_id)

@app.put("/api/locations/{item_id}")
def update_location(item_id: int, item: schemas.LocationIn, db: Session = Depends(get_db)):
    obj = db.query(models.Location).get(item_id)
    if not obj: return {"error":"not found"}
    for k,v in item.model_dump(exclude_unset=True).items(): setattr(obj,k,v)
    db.commit(); db.refresh(obj); return obj

@app.delete("/api/locations/{item_id}")
def delete_location(item_id: int, db: Session = Depends(get_db)):
    obj = db.query(models.Location).get(item_id)
    if not obj: return {"ok": False}
    db.delete(obj); db.commit(); return {"ok": True}

