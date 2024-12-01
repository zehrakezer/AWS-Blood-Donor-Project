from typing import List
import fastapi as _fastapi
import fastapi.security as _security
import httpx
import sqlalchemy.orm as _orm
from fastapi import HTTPException
import services as _services, schemas as _schemas
from database import engine, Base
import models as _models
from fastapi.middleware.cors import CORSMiddleware

# FastAPI uygulaması oluşturuluyor
app = _fastapi.FastAPI()

# CORS Middleware ekleniyor
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tüm kaynaklara izin ver
    allow_credentials=True,  # Kimlik bilgilerine izin ver
    allow_methods=["*"],  # Tüm HTTP metotlarına izin ver
    allow_headers=["*"],  # Tüm başlıklara izin ver
)

# Veritabanı tabloları oluşturuluyor
Base.metadata.create_all(bind=engine)

# Email gönderim fonksiyonları
async def sendEmail(email):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://11.execute-api.eu-central-1.amazonaws.com/default/savemailadress",
                params={"email": email}
            )
            response.raise_for_status()
            print("HTTP Request successful:", response.json())
    except httpx.HTTPStatusError as exc:
        print(f"HTTP Request failed with status {exc.response.status_code}: {exc.response.text}")
    except Exception as e:
        print(f"Unexpected error during HTTP request: {e}")


async def sendEmail2(id):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://ss.execute-api.eu-central-1.amazonaws.com/default/newuserpublication",
                params={"user_id": id}
            )
            response.raise_for_status()
            print("HTTP Request successful:", response.json())
    except httpx.HTTPStatusError as exc:
        print(f"HTTP Request failed with status {exc.response.status_code}: {exc.response.text}")
    except Exception as e:
        print(f"Unexpected error during HTTP request: {e}")


# API endpointleri
@app.post("/api/users")
async def create_user(
    user: _schemas.UserCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    db_user = await _services.get_user_by_email(user.email, db)
    if db_user:
        raise _fastapi.HTTPException(status_code=400, detail="Email already in use")
    else:
        try:
            await sendEmail(user.email)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to send email: {str(e)}"
            )

    user = await _services.create_user(user, db)
    return await _services.create_token(user)


@app.post("/api/token")
async def generate_token(
    form_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends(),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    user = await _services.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise _fastapi.HTTPException(status_code=401, detail="Hatalı Giriş Yaptınız.!")

    return await _services.create_token(user)


@app.get("/api/users/me", response_model=_schemas.User)
async def get_user(user: _schemas.User = _fastapi.Depends(_services.get_current_user)):
    return user


@app.post("/api/leads", response_model=_schemas.Lead)
async def create_lead(
    lead: _schemas.LeadCreate,
    user: _schemas.User = _fastapi.Depends(_services.get_current_user),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    return await _services.create_lead(user=user, db=db, lead=lead)


@app.get("/api/leads", response_model=List[_schemas.Lead])
async def get_leads(
    user: _schemas.User = _fastapi.Depends(_services.get_current_user),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    return await _services.get_leads(user=user, db=db)


@app.get("/api/leads/{lead_id}", status_code=200)
async def get_lead(
    lead_id: int,
    user: _schemas.User = _fastapi.Depends(_services.get_current_user),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    return await _services.get_lead(lead_id, user, db)


@app.delete("/api/leads/{lead_id}", status_code=204)
async def delete_lead(
    lead_id: int,
    user: _schemas.User = _fastapi.Depends(_services.get_current_user),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    await _services.delete_lead(lead_id, user, db)
    return {"message": "Successfully Deleted"}


@app.put("/api/leads/{lead_id}", status_code=200)
async def update_lead(
    lead_id: int,
    lead: _schemas.LeadCreate,
    user: _schemas.User = _fastapi.Depends(_services.get_current_user),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    await _services.update_lead(lead_id, lead, user, db)
    return {"message": "Successfully Updated"}


@app.get("/api")
async def root():
    return {"message": "Grup 4"}


# Diğer endpointler aşağıdaki formatta devam ediyor...

@app.get("/api/blood-types", response_model=List[_schemas.BloodType])
async def get_blood_types(db: _orm.Session = _fastapi.Depends(_services.get_db)):    
    blood_types = db.query(_models.BloodType).all()
    print("\n\n#############\n\n",blood_types)
    return blood_types 

@app.get("/api/donation_type", response_model=List[_schemas.DonationType])
async def get_donation_types(db: _orm.Session = _fastapi.Depends(_services.get_db)):    
    donation_type = db.query(_models.DonationType).all()
    print("\n\n#############\n\n",donation_type)
    return donation_type

# Get all cities
@app.get("/api/cities", response_model=List[_schemas.City])
async def get_cities(db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return _services.get_cities(db)

# Get districts by city ID
@app.get("/api/districts/{city_id}", response_model=List[_schemas.District])
async def get_districts_by_city(city_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return _services.get_districts_by_city(city_id, db)

# Get neighborhoods by district ID
@app.get("/api/neighborhoods/{district_id}", response_model=List[_schemas.NeighborhoodBase])
async def get_neighborhoods_by_district(district_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return _services.get_neighborhoods_by_district(district_id, db)





@app.post("/create-request", status_code=_fastapi.status.HTTP_201_CREATED)
async def create_ilan(
    request: _schemas.BloodilanRequest1, 
    db: _orm.Session = _fastapi.Depends(_services.get_db)):

    print("/create-request endpoint hit.")

    data = request.dict()
    print("received data",data)
    # Kullanıcıyı kontrol et
    user = await _services.get_userID_by_email(data['email'], db)
    if not user:
        raise _fastapi.HTTPException(
            status_code=_fastapi.status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
        
    #send E-Mail 
    try:
        print("\n\n\n #### Email sending, \n\nuserid:",user)
        await sendEmail2(user)  
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to send email: {str(e)}"
        )
    
    print(f"\n\nUser found with ID: {user}")
    print("Request data['donation_type']:",data['donationType'])
    print("Request data['blood_type_id']:",data['blood_type_id'])
    print("Request data['urgency_status']:",data['urgency_status'])


    if data['donationType'] == "Tam kan bağışı":
        data['donationType'] = "1"
    elif data['donationType'] =="Tromboferez":
        data['donationType'] = "2"
    elif data['donationType'] =="Eritroferez":
        data['donationType'] = "3"
    elif data['donationType'] =="Plazmaferez":
        data['donationType'] = "4"
    else: data['donationType'] = "1"

    

    # data['bloodType']=1
    # data['donation_type']=1
    
   
    data['email_service']=0
    print("email_service",data)


    ##opener
    opener = await _services.get_opener_by_email(data['email'], db)
    
    ## save db
    ilanSave = await _services.create_publication(user,data,opener, db)
    
    return ilanSave


def transform_publication(publication):
    return {
        "id": publication.id,
        "user_id": publication.user_id,
        "hospital_name": publication.hospital_name,
        "blood_type_id": publication.blood_type_id,
        "urgency_status": publication.urgency_status,
        "start_date": publication.start_date.isoformat() if publication.start_date else None,
        "end_date": publication.end_date.isoformat() if publication.end_date else None,
        "create_date": publication.end_date.isoformat() if publication.end_date else None,
        "donation_type": publication.donation_type, 
        "description": publication.description,
        "status": publication.status,
        "location": publication.location,
    }

@app.get("/blood-donation-publications/{email}", response_model=List[_schemas.BloodilanRequest])
async def get_all_publications(email: str, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    user_id = await _services.get_userID_by_email(email, db)
    print("user_id",user_id)

    publications = db.query(_models.BloodDonationPublication).all()
    Ilanlist=[transform_publication(pub) for pub in publications]    

    return Ilanlist


from sqlalchemy.orm import joinedload

def get_neighborhood_details_by_id(neighborhood_id: int, db: _orm.Session):
    """
    Returns city.name, district.name, and neighborhood.name based on the neighborhood ID.
    """
    # Query the Neighborhood model, joining with District and City
    neighborhood = db.query(_models.Neighborhood).options(
        joinedload(_models.Neighborhood.district).joinedload(_models.District.city)  # Join District and City
    ).filter(_models.Neighborhood.id == neighborhood_id).first()

    # If no neighborhood is found, return None
    if not neighborhood:
        return None

    # Access related data through relationships
    city_name = neighborhood.district.city.name
    district_name = neighborhood.district.name
    neighborhood_name = neighborhood.name

    addres=f"{city_name}/{district_name}/{neighborhood_name}"
    # print("addres",addres)

    return addres



@app.get("/self-blood-donation-publications/{email}", response_model=List[_schemas.reBloodilanRequest])
async def get_all_publications(email: str, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    user_id = await _services.get_userID_by_email(email, db)
    print("user_id",user_id)

    self_publications = (
    db.query(_models.BloodDonationPublication)
    .filter(_models.BloodDonationPublication.user_id == user_id)
    .all()
    ) 
   
    for pub in self_publications:        
        location_details = get_neighborhood_details_by_id(pub.location, db)
        if location_details:
            pub.location2 = location_details
        else:
            pub.location2 = "Location details not found"
    #Ilanlist=[transform_publication(pub) for pub in self_publications]
    # print("Ilanlist",self_publications)    

    return self_publications



@app.get("/other-blood-donation-publications/{email}", response_model=List[_schemas.reBloodilanRequest])
async def get_all_publications(email: str, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    user_id = await _services.get_userID_by_email(email, db)
    print("user_id",user_id)

    other_publications = (
    db.query(_models.BloodDonationPublication)
    .filter(_models.BloodDonationPublication.user_id != user_id)
    .all()
    )    
    
    for pub in other_publications:             
       
        location_details = get_neighborhood_details_by_id(pub.location, db)
        if location_details:
            pub.location2 = location_details
        else:
            pub.location2 = "Location details not found"
    #Ilanlist=[transform_publication(pub) for pub in other_publications]
    # print("Ilanlist",Ilanlist)

    return other_publications


@app.get("/apply-publications/{id}/{email}/{location}")  #,response_model=List[_schemas.BloodilanRequest]
async def applied_publications(id: int, email: str, location:int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    print("\n\n\nid email",id)
    user_id = await _services.get_userID_by_email(email, db)
    print("user_id",user_id)

    publication = db.query(_models.BloodDonationPublication).filter_by(user_id=id , location=location).first()
    print("publication", publication.id, publication.user_id, publication.aplication_user_id )

    #opener applied
    applied = await  _services.get_namePhone_by_email(email, db)
    opener = await  _services.get_namePhone_by_ID(id, db)
    if publication:
        publication.aplication_user_id = user_id
        publication.applied = applied
        publication.opener = opener
        publication.status = 1
        db.commit()
        print(f"Publication ID {id} için application_user_id {user_id} olarak güncellendi.")
    else:
        print(f"Publication ID {id} bulunamadı.")



@app.get("/delete-publications/{id}/{email}/{location}")  #,response_model=List[_schemas.BloodilanRequest]
async def delete_publications(id: int, email: str, location:int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    print("\n\n\nid --->",id)
    #user_id = await _services.get_userID_by_email(email, db)
    #print("user_id",user_id)

    publication = db.query(_models.BloodDonationPublication).filter_by(user_id=id , location=location).first()
    print("publication", publication.id, publication.user_id)


    if not publication:
        # Yayın bulunamazsa hata döndür
        raise _fastapi.HTTPException(status_code=404, detail="Publication not found")

  
    # Yayını veritabanından sil
    db.delete(publication)
    db.commit()
 
    return {"detail": "Publication deleted successfully"}
    
