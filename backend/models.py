import datetime as _dt
import sqlalchemy as _sql
import sqlalchemy.orm as _orm
import passlib.hash as _hash
import database as _database
from sqlalchemy import Column, Integer, String, Enum, Date, DateTime, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property

# old table
############################################################################
# class User(_database.Base):
#     __tablename__ = "users"
#     id = _sql.Column(_sql.Integer, primary_key=True, index=True)
#     email = _sql.Column(_sql.String, unique=True, index=True)
#     hashed_password = _sql.Column(_sql.String)

#     leads = _orm.relationship("Lead", back_populates="owner")

#     def verify_password(self, password: str):
#         return _hash.bcrypt.verify(password, self.hashed_password)

#########################################################################

class User(_database.Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(255), nullable=True)
    surname = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(255), nullable=True)
    location = Column(Integer, ForeignKey("neighborhood.id"), nullable=True)
    blood_type_id = Column(Integer, ForeignKey("blood_type.id"), nullable=True)
    gender = Column(Enum("Male", "Female", "Other"), nullable=True)
    birth_date = Column(Date, nullable=True)
    weight = Column(Integer, nullable=True)
    is_donor = Column(Enum("Yes", "No"), nullable=True)
    can_donate = Column(Enum("Yes", "No"), nullable=True)
    agreed_terms = Column(Enum("Yes", "No"), nullable=True)
    hashed_password = Column(String, nullable=False)
    status = Column(Integer, nullable=True)
    created_date = Column(DateTime, nullable=True)
    updated_date = Column(DateTime, nullable=True)
    
    #updated_by = Column(Integer, ForeignKey("admin.id"), nullable=True)

    #Relationships
    leads = _orm.relationship("Lead", back_populates="owner")
       
   
    blood_type = _orm.relationship("BloodType", back_populates="users")
    health_forms = _orm.relationship("HealthForms", back_populates="user")
    audit_logs = _orm.relationship("AuditLogs", back_populates="user")
    blood_donations = _orm.relationship("BloodDonationPublication", back_populates="user")

    # new Relationships
    #neighborhood = _orm.relationship("Neighborhood", back_populates="users")
    #updated_by_admin = _orm.relationship("Admin", back_populates="updated_users")
    #chosen_donations = _orm.relationship("BloodDonChosen", back_populates="user")
    #donation_applications = _orm.relationship("BloodDonApplicant", back_populates="user")

    def verify_password(self, password: str):
        return _hash.bcrypt.verify(password, self.hashed_password)


class Lead(_database.Base):
    __tablename__ = "leads"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    #owner_id = _sql.Column(_sql.Integer, _sql.ForeignKey("users.id"))  ## from old table 
    owner_id = _sql.Column(_sql.Integer, _sql.ForeignKey("User.id"))
    first_name = _sql.Column(_sql.String, index=True)
    last_name = _sql.Column(_sql.String, index=True)
    email = _sql.Column(_sql.String, index=True)
    company = _sql.Column(_sql.String, index=True, default="")
    note = _sql.Column(_sql.String, default="")
    date_created = _sql.Column(_sql.DateTime, default=_dt.datetime.now)
    date_last_updated = _sql.Column(_sql.DateTime, default=_dt.datetime.now)

    owner = _orm.relationship("User", back_populates="leads")



class City(_database.Base):
    __tablename__ = 'city'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255))  
    
    # Add __repr__ method to avoid cyclic references when serializing
    def __repr__(self):
        return f"<City(id={self.id}, name={self.name})>"

class District(_database.Base):
    __tablename__ = 'district'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255))  
    city_id = Column(Integer, ForeignKey('city.id'))  
    city = _orm.relationship('City', backref='district')
    
    # Add __repr__ method to avoid cyclic references when serializing
    def __repr__(self):
        return f"<District(id={self.id}, name={self.name}, city_id={self.city_id})>"

class Neighborhood(_database.Base):
    __tablename__ = 'neighborhood'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255))  
    district_id = Column(Integer, ForeignKey('district.id'))
    district = _orm.relationship('District', backref='neighborhood')
    #users = _orm.relationship("User", back_populates="neighborhood")  # Relationship with User
    
    # Add __repr__ method to avoid cyclic references when serializing
    def __repr__(self):
        return f"<Neighborhood(id={self.id}, name={self.name}, district_id={self.district_id})>"


class BloodType(_database.Base):
    __tablename__ = "blood_type"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(255), nullable=False, unique=True)

    # Relationship
    users = _orm.relationship("User", back_populates="blood_type")
    blood_donations = _orm.relationship("BloodDonationPublication", back_populates="blood_type_r")



    


class AuditLogs(_database.Base):
    __tablename__ = "Audit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, ForeignKey("User.id"), nullable=False)
    #admins_id = Column(Integer, ForeignKey("Admin.id"), nullable=True)
    login_status = Column(Enum("Success", "Failure"), nullable=False)
    created_date = Column(DateTime, nullable=False)

    user = _orm.relationship("User", back_populates="audit_logs")
    #admin = _orm.relationship("Admin", back_populates="audit_logs")


class DonationType(_database.Base):
    __tablename__ = "donation_type"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(255), nullable=False, unique=True)

    blood_donations = _orm.relationship("BloodDonationPublication", back_populates="donation_type_relation")


class HealthForms(_database.Base):
    __tablename__ = "Health_Forms"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, ForeignKey("User.id"), nullable=False)
    answer = Column(Enum("Yes", "No"), nullable=False)
    status = Column(Integer, nullable=True)
    created_date = Column(DateTime, nullable=True)
    updated_date = Column(DateTime, nullable=True)
    #updated_by = Column(Integer, ForeignKey("Admin.id"), nullable=True)

    user = _orm.relationship("User", back_populates="health_forms")
    #updated_by_admin = _orm.relationship("Admin", back_populates="updated_health_forms")




#  neighborhood: form.neighborhood,
#     hospital: form.hospital,
#     bloodType: form.bloodType,
#     demandStatus: form.demandStatus,
#     annotation: form.annotation,
#     startDate: form.startDate,
#     finishDate: form.finishDate,
#     donationType: form.donationType,







class BloodDonationPublication(_database.Base):
    __tablename__ = "Blood_Donation_Publication"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, ForeignKey("User.id"), nullable=False)
    hospital_name = Column(String(255), nullable=True)
    blood_type_id = Column(Integer, ForeignKey("blood_type.id"), nullable=False)
    urgency_status = Column(Integer, nullable=False)  # 1: Acil, 2: Planlı
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    created_date = Column(DateTime, nullable=True)
    donation_type = Column(Integer, ForeignKey("donation_type.id"), nullable=False)
    description = Column(String(255), nullable=True)
    status = Column(Integer, nullable=False)  # 1: Başarılı, 2: Başarısız, 3: Devam Eden
    location = Column(Integer, nullable=False)  
    location2 = Column(String, nullable=True)  
    aplication_user_id = Column(Integer, nullable=True)
    email_service = Column(Integer, nullable=True)
    opener = Column(String, nullable=True)  
    applied = Column(String, nullable=True)  


    # Relationships
    user = _orm.relationship("User", back_populates="blood_donations")  # Foreign key ilişkisi
    blood_type_r = _orm.relationship("BloodType", back_populates="blood_donations")  # Tek bir ilişki
    donation_type_relation = _orm.relationship("DonationType", back_populates="blood_donations")


   




