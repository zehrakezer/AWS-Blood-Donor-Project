import datetime as _dt
from datetime import date
import pydantic as _pydantic
from typing import Optional, List
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, validator







# Kan Bağışı Talebi Şeması
class BloodilanRequest(_pydantic.BaseModel):
    user_id:int
    neighborhood: Optional[str] = None 
    hospital_name: Optional[str] = None 
    blood_type_id: Optional[int] = None 
    urgency_status: Optional[int] = None 
    annotation: Optional[str] = None 
    start_date:Optional[datetime] = None 
    end_date: Optional[datetime] = None  
    created_date: Optional[datetime] = None
    donation_type: Optional[int] = None 
    description: Optional[str] = None 
    email: Optional[str] = None 
    location: Optional[int] = None 
    status: Optional[int] = None 
    opener: Optional[str] = None 
    applied: Optional[str] = None 

class BloodilanRequest1(_pydantic.BaseModel):    
    hospital: Optional[str] = None 
    blood_type_id: Optional[int] = None 
    urgency_status: Optional[str] = None 
    annotation: Optional[str] = None 
    start_date:Optional[datetime] = None 
    finish_date: Optional[datetime] = None  
    created_date: Optional[datetime] = None  
    donationType: Optional[str] = None 
    email: Optional[str] = None 
    neighborhood: Optional[int] = None 
    # location: Optional[int] = None 
    aplication_user_id: Optional[int] = None 
    email_service: Optional[int] = None 
    status: Optional[int] = None 
    opener: Optional[str] = None 
    applied: Optional[str] = None 
    


class reBloodilanRequest(_pydantic.BaseModel):
    user_id:int
    neighborhood: Optional[str] = None 
    hospital_name: Optional[str] = None 
    blood_type_id: Optional[int] = None 
    urgency_status: Optional[int] = None 
    # annotation: Optional[str] = None 
    start_date:Optional[datetime] = None 
    end_date: Optional[datetime] = None  
    created_date: Optional[datetime] = None
    donation_type: Optional[int] = None 
    description: Optional[str] = None 
    email: Optional[str] = None 
    location: Optional[int] = None 
    location2: Optional[str] = None 
    status: Optional[int] = None 
    opener: Optional[str] = None 
    applied: Optional[str] = None 


   

class GenderEnum(str, Enum):
    male = "Male"
    female = "Female"
    other = "Other"




class YesNoEnum(str, Enum):
    yes = "Yes"
    no = "No"


class _UserBase(_pydantic.BaseModel):
    id: Optional[int]
    name: str
    surname:str
    email: str
    phone:str
    location:int
    blood_type_id:int
    gender:GenderEnum  
    birth_date:date
    weight:int
    is_donor: bool
    can_donate:bool
    agreed_terms:bool
    hashed_password:str
    status:int
    created_date:Optional[date] = None
    updated_date:Optional[date] = None



class UserCreate(_UserBase):
    pass
    # hashed_password: str

    # class Config:
    #     from_attributes = True


class User(_UserBase):
    id: int
    

    class Config:
        from_attributes = True


class _LeadBase(_pydantic.BaseModel):
    first_name: str
    last_name: str
    email: str
    company: str
    note: str


class LeadCreate(_LeadBase):
    pass


class Lead(_LeadBase):
    id: int
    owner_id: int
    date_created: _dt.datetime
    date_last_updated: _dt.datetime

    class Config:
        from_attributes = True



class BloodTypeBase(_pydantic.BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class BloodType(BloodTypeBase):
    id: int

    class Config:
        from_attributes = True


class CityBase(_pydantic.BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class City(CityBase):
    id: int
    districts: List["District"] = []

    class Config:
        from_attributes = True


class DistrictBase(_pydantic.BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class District(DistrictBase):
    id: int
    city_id: int
    city: City
    neighborhoods: List["Neighborhood"] = []

    class Config:
        from_attributes = True


class NeighborhoodBase(_pydantic.BaseModel):
    id: int
    name: str
    district_id: int
    district: DistrictBase  

    class Config:
        from_attributes = True


class Neighborhood(NeighborhoodBase):
    id: int
    district_id: int
    district: District
    users: List["User"] = []

    class Config:
        from_attributes = True


class AuditLogBase(_pydantic.BaseModel):
    id: int
    login_status: str
    created_date: _dt.datetime

    class Config:
        from_attributes = True


class AuditLog(AuditLogBase):
    user_id: int
    user: User

    class Config:
        from_attributes = True


class DonationTypeBase(_pydantic.BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class DonationType(DonationTypeBase):
    id: int

    class Config:
        from_attributes = True
