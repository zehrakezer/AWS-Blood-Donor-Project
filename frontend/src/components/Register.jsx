import React, { useContext, useState, useEffect } from "react";
import { UserContext } from "../context/UserContext";
import ErrorMessage from "./ErrorMessage";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";



const Register = () => {
  const navigate = useNavigate(); // useNavigate hook
  const [cities, setCities] = useState([]);
  const [districts, setDistricts] = useState([]);
  const [neighborhoods, setNeighborhoods] = useState([]);

  const [city, setCity] = useState("");
  const [district, setDistrict] = useState("");
  const [neighborhood, setNeighborhood] = useState("");

  const [name, setName] = useState("");
  const [surname, setSurname] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [gender, setGender] = useState("Male");
  const [birthDate, setBirthDate] = useState("");
  const [weight, setWeight] = useState("");
  const [bloodType, setBloodType] = useState("");
  const [isDonor, setIsDonor] = useState(1);
  const [canDonate, setCanDonate] = useState(1);
  const [agreedTerms, setAgreedTerms] = useState(1);
  const [password, setPassword] = useState("");
  const [confirmationPassword, setConfirmationPassword] = useState("");
  const [bloodTypes, setBloodTypes] = useState([]);
  const [errorMessage, setErrorMessage] = useState("");
  const [, setToken] = useContext(UserContext);

  useEffect(() => {
    const fetchCities = async () => {
      const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/api/cities`);
      const data = await response.json();
      setCities(data);
    };

    fetchCities();
  }, []);

  const handleCityChange = async (event) => {
    setCity(event.target.value);
    const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/api/districts/${event.target.value}`);
    const data = await response.json();
    setDistricts(data);
  };

  const handleDistrictChange = async (event) => {
    setDistrict(event.target.value);
    const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/api/neighborhoods/${event.target.value}`);
    const data = await response.json();
    setNeighborhoods(data);
  };

  useEffect(() => {
    const fetchBloodTypes = async () => {
      const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/api/blood-types`);
      const data = await response.json();
      setBloodTypes(data);
    };

    fetchBloodTypes();
  }, []);

  const formatPhoneNumber = (value) => {
    // Sadece rakamları al
    const digits = value.replace(/\D/g, "");
    // Formatı uygula: (XXX) XXX-XX-XX
    const formatted =
      digits.length <= 3
        ? digits
        : digits.length <= 6
        ? `(${digits.slice(0, 3)}) ${digits.slice(3)}`
        : digits.length <= 8
        ? `(${digits.slice(0, 3)}) ${digits.slice(3, 6)}-${digits.slice(6)}`
        : `(${digits.slice(0, 3)}) ${digits.slice(3, 6)}-${digits.slice(
            6,
            8
          )}-${digits.slice(8, 10)}`;
    return formatted;
  };

  const handlePhoneChange = (e) => {
    const formattedPhone = formatPhoneNumber(e.target.value);
    setPhone(formattedPhone);
  };

  const submitRegistration = async () => {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        id: -1,
        status:1,
        name,
        surname,
        email,
        phone,
        gender,
        birth_date: birthDate,
        weight,
        blood_type_id: bloodType,
        is_donor: isDonor,
        can_donate: canDonate,
        agreed_terms: agreedTerms,
        hashed_password: password,
        location: neighborhood,
      }),
    };

    const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/api/users`, requestOptions);
    console.log("response",response)
    const data = await response.json();
    

    if (!response.ok) {
      setErrorMessage(data.detail);
    } else {
      // setToken(data.access_token);
      // logout();
      alert("Kayıt işlemi başarılı. Giriş yapınız!")
      navigate("/");
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (password === confirmationPassword && password.length > 5) {
      submitRegistration();
    } else {
      setErrorMessage(
        "Ensure that the passwords match and are greater than 5 characters."
      );
    }
  };

  return (
    <div className="column">
      <form className="box" onSubmit={handleSubmit}>
        <h1 className="title has-text-centered">ÜYE OL</h1>
        {/* City, District, and Neighborhood Selection */}
        <div className="columns">
          <div className="field column">
            <label className="label">İL</label>
            <div className="control select" style={{ width: "100%" }}>
              <select
                value={city}
                onChange={handleCityChange}
                className="select"
                required
                style={{ width: "100%" }}
              >
                <option value="">seçiniz</option>
                {cities.map((cityItem) => (
                  <option key={cityItem.id} value={cityItem.id}>
                    {cityItem.name}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="field column">
            <label className="label">İLÇE</label>
            <div className="control select" style={{ width: "100%" }}>
              <select
                value={district}
                onChange={handleDistrictChange}
                className="select"
                required
                style={{ width: "100%" }}
              >
                <option value="">seçiniz</option>
                {districts.map((districtItem) => (
                  <option key={districtItem.id} value={districtItem.id}>
                    {districtItem.name}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>

        <div className="columns">
          <div className="field column">
            <label className="label">MAHALLE</label>
            <div className="control select" style={{ width: "100%" }}>
              <select
                value={neighborhood}
                onChange={(e) => setNeighborhood(e.target.value)}
                className="select"
                required
                style={{ width: "100%" }}
              >
                <option value="">Mahalle seçiniz</option>
                {neighborhoods.map((neighborhoodItem) => (
                  <option key={neighborhoodItem.id} value={neighborhoodItem.id}>
                    {neighborhoodItem.name}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="field column">
            <label className="label">CİNSİYET</label>
            <div className="control select" style={{ width: "100%" }}>
              <select
                value={gender}
                onChange={(e) => setGender(e.target.value)}
                className="select"
                required
                style={{ width: "100%" }}
              >
                <option value="Male">Erkek</option>
                <option value="Female">Kadın</option>
              </select>
            </div>
          </div>
        </div>

        <div className="columns">
          <div className="field column">
            <label className="label">AD</label>
            <div className="control">
              <input
                type="text"
                placeholder="Adınızı giriniz"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="input"
                required
              />
            </div>
          </div>
          <div className="field column">
            <label className="label">SOYAD</label>
            <div className="control">
              <input
                type="text"
                placeholder="Soyadınızı giriniz"
                value={surname}
                onChange={(e) => setSurname(e.target.value)}
                className="input"
                required
              />
            </div>
          </div>
        </div>
        <div className="columns">
          <div className="field column">
            <label className="label">EMAİL</label>
            <div className="control">
              <input
                type="email"
                placeholder="Email giriniz"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="input"
                required
              />
            </div>
          </div>
          <div className="field column">
            <label className="label">TELEFON NUMARASI</label>
            <div className="control">
              <input
                type="text"
                placeholder="Telefon numarası giriniz"
                value={phone}
                onChange={handlePhoneChange}
                className="input"
              />
            </div>
          </div>
        </div>
        <div className="columns">
          <div className="field column">
            <label className="label">DOĞUM TARİHİ</label>
            <div className="control">
              <input
                type="date"
                value={birthDate}
                onChange={(e) => setBirthDate(e.target.value)}
                className="input"
              />
            </div>
          </div>
          <div className="field column">
            <label className="label">KİLO</label>
            <div className="control">
              <input
                type="number"
                value={weight}
                onChange={(e) => setWeight(e.target.value)}
                className="input"
              />
            </div>
          </div>
        </div>
        <div className="columns">
          <div className="field column">
            <label className="label">ŞİFRE</label>
            <div className="control">
              <input
                type="password"
                placeholder="Şifrenizi giriniz"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="input"
                required
              />
            </div>
          </div>
          <div className="field column">
            <label className="label">ŞİFRE (TEKRAR)</label>
            <div className="control">
              <input
                type="password"
                placeholder="Şifre tekrar"
                value={confirmationPassword}
                onChange={(e) => setConfirmationPassword(e.target.value)}
                className="input"
                required
              />
            </div>
          </div>
        </div>
        <div className="columns">
          <div className="field column">
            <label className="label">KAN GRUBU</label>
            <div className="control select">
              <select
                value={bloodType}
                onChange={(e) => setBloodType(e.target.value)}
                className="select"
                required
              >
                <option value="">Kan grubu seçiniz</option>
                {bloodTypes.map((blood) => (
                  <option key={blood.id} value={blood.id}>
                    {blood.name}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>
        
        
        <ErrorMessage message={errorMessage} />
        <br />
        <Link to="/login">Hesabınız var mı ?</Link>
        <br />
        <br />
        <button className="button is-primary" type="submit">
          ÜYE OL
        </button>
      </form>
    </div>
  );
};

export default Register;
