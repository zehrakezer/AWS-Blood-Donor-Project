import fastapi as _fastapi
import fastapi.security as _security
import jwt as _jwt
import datetime as _dt
import sqlalchemy.orm as _orm
import passlib.hash as _hash
from sqlalchemy.orm import joinedload
import database as _database, models as _models, schemas as _schemas






oauth2schema = _security.OAuth2PasswordBearer(tokenUrl="/api/token")

JWT_SECRET = "myjwtsecret"




def create_database():
    return _database.Base.metadata.create_all(bind=_database.engine)


def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_user_by_email(email: str, db: _orm.Session):
    print("email",email)
    ask=db.query(_models.User).filter(_models.User.email == email).first()
    print("ask",ask)
    return ask

async def get_userID_by_email(email: str, db: _orm.Session):
    print("email", email)
    user = db.query(_models.User.id).filter(_models.User.email == email).first()
    
    if user:
        print("Kullanıcı ID:", user.id)
        return user.id 
    else:
        print("Kullanıcı bulunamadı.")
        return None 

async def create_user(user: _schemas.UserCreate, db: _orm.Session):
    print("user",user)
    user_obj = _models.User(
        email=user.email, 
        hashed_password=_hash.bcrypt.hash(user.hashed_password),
        name=user.name,
        surname=user.surname,
        phone=user.phone,
        location=user.location,
        blood_type_id=user.blood_type_id,
        gender=user.gender,
        birth_date=user.birth_date,
        weight=user.weight,
        is_donor="No",
        can_donate="No",
        agreed_terms="Yes",
        status=1,
        created_date= _dt.datetime.now().date()

    )    
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj


async def authenticate_user(email: str, password: str, db: _orm.Session):
    print("authenticate_user,user,email,password")
    print(email,password)
    user = await get_user_by_email(db=db, email=email)
    print("user,email,password")
    print(user,email,password)
    if not user:
        return False
    # if not user.verify_password(password):
    #     return False

    return user


async def create_token(user: _models.User):
    print("create_token")
    _json = {
        "email": user.email,
        "id": user.id
    }
    token = _jwt.encode(_json, JWT_SECRET)
    print("token",token)


    return dict(access_token=token, token_type="bearer")


async def get_current_user(
    db: _orm.Session = _fastapi.Depends(get_db),
    token: str = _fastapi.Depends(oauth2schema),
):
    try:
        print("get user")
        print("token",token)
        JWT_SECRET = "myjwtsecret"
        payload = _jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        print("payload",payload)
        user = db.query(_models.User).get(payload["id"])
        print(" user",user)

    except:
        print("Except ")
        raise _fastapi.HTTPException(
            status_code=401, detail="Invalid Email or Password"
        )

    return _schemas.User.from_orm(user)


async def create_lead(user: _schemas.User, db: _orm.Session, lead: _schemas.LeadCreate):
    lead = _models.Lead(**lead.dict(), owner_id=user.id)
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return _schemas.Lead.from_orm(lead)


async def get_leads(user: _schemas.User, db: _orm.Session):
    leads = db.query(_models.Lead).filter_by(owner_id=user.id)

    return list(map(_schemas.Lead.from_orm, leads))


async def _lead_selector(lead_id: int, user: _schemas.User, db: _orm.Session):
    lead = (
        db.query(_models.Lead)
        .filter_by(owner_id=user.id)
        .filter(_models.Lead.id == lead_id)
        .first()
    )

    if lead is None:
        raise _fastapi.HTTPException(status_code=404, detail="Lead does not exist")

    return lead


async def get_lead(lead_id: int, user: _schemas.User, db: _orm.Session):
    lead = await _lead_selector(lead_id=lead_id, user=user, db=db)

    return _schemas.Lead.from_orm(lead)


async def delete_lead(lead_id: int, user: _schemas.User, db: _orm.Session):
    lead = await _lead_selector(lead_id, user, db)

    db.delete(lead)
    db.commit()

async def update_lead(lead_id: int, lead: _schemas.LeadCreate, user: _schemas.User, db: _orm.Session):
    lead_db = await _lead_selector(lead_id, user, db)

    lead_db.first_name = lead.first_name
    lead_db.last_name = lead.last_name
    lead_db.email = lead.email
    lead_db.company = lead.company
    lead_db.note = lead.note
    lead_db.date_last_updated = _dt.datetime.now()

    db.commit()
    db.refresh(lead_db)

    return _schemas.Lead.from_orm(lead_db)



def get_cities(db: _orm.Session):
    # Returns all cities
    cities = db.query(_models.City).all()
    return cities

def get_districts_by_city(city_id: int, db: _orm.Session):
    # Returns districts by city ID (correct filter)
    districts = db.query(_models.District).filter(_models.District.city_id == city_id).all()
    return districts

def get_neighborhoods_by_district(district_id: int, db: _orm.Session):
    neighborhoods = db.query(_models.Neighborhood).options(
        joinedload(_models.Neighborhood.district)  # Apply joinedload to the district relationship
    ).filter(_models.Neighborhood.district_id == district_id).all()
    return neighborhoods



async def create_publication(thatUser,publication_data: _schemas.BloodilanRequest, opener,db: _orm.Session):
    
    print("int(publication_data['neighborhood']),",int(publication_data['neighborhood']))
    
    if publication_data['urgency_status'] =="Acil":
        IsAcil=1
    else: IsAcil=2
    
    # Yeni ilan nesnesi
    publication_obj = _models.BloodDonationPublication(
      
        user_id=thatUser,
        hospital_name=publication_data['hospital'],
        blood_type_id=publication_data['blood_type_id'],
        #blood_type=blood_type,
        urgency_status=IsAcil,
        # urgency_status=1,
        created_date=_dt.datetime.now(),
        start_date=publication_data.get('startDate', None) if publication_data.get('startDate', None) is not None else _dt.datetime.now(),
        end_date=publication_data.get('finishDate', None) if publication_data.get('finishDate', None) is not None else _dt.datetime.now(),
        donation_type=int(publication_data['donationType']),
        location=int(publication_data['neighborhood']),
        description=publication_data['annotation'],
        status=0,
        aplication_user_id = 0,
        email_service = 0,
        opener=opener,
        applied="---",
    )

    # Veritabanına kaydet
    db.add(publication_obj)
    db.commit()
    db.refresh(publication_obj)

    return publication_obj


from sqlalchemy import select

async def get_namePhone_by_email(email: str, db: _orm.Session):
    print("Sorgulanan email:", email)
        
    result = db.execute(
        select(_models.User).where(_models.User.email == email)
    )
    user = result.scalar_one_or_none()

    if not user:
        print("Kullanıcı bulunamadı.")
        return None

    applied = f"{user.name} {user.surname} - {user.phone}"
    print("Ilani acan Kullanıcı Bilgisi:", applied)
    return applied
    

async def get_namePhone_by_ID(id: int, db: _orm.Session):
    print("Sorgulanan ID:", id)
        
    result = db.execute(
        select(_models.User).where(_models.User.id == id)
    )
    user = result.scalar_one_or_none()

    if not user:
        print("Kullanıcı bulunamadı.")
        return None

    opener = f"{user.name} {user.surname} - {user.phone}"
    print("Ilani acan Kullanıcı Bilgisi:", opener)
    return opener


async def get_opener_by_email(email: str, db: _orm.Session):
    print("Ilan acan email:", email)
        
    result = db.execute(
        select(_models.User).where(_models.User.email == email)
    )
    user = result.scalar_one_or_none()

    if not user:
        print("Kullanıcı bulunamadı.")
        return None

    opener = f"{user.name} {user.surname} - {user.phone}"
    print("Ilani acan Kullanıcı Bilgisi:", opener)
    return opener