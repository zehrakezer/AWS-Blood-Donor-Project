import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom"; // Import useNavigate
import { useLocation } from "react-router-dom";


const AdsComponent = () => {
  const location = useLocation();
  const email = location.state?.email; 
  console.log("ADS Comp Who are u?", email)
  const navigate = useNavigate(); // useNavigate hook
  // const [email, setEmail] = useState("user@example.com");
  const INITIAL_STATE = {
    city: "",
    district: "",
    districts: [],
    neighborhood: "",
    neighborhoods: [],
    hospital: "",
    blood_type_id: "",
    bloodTypes: [],
    urgency_status: "",
    // bloodDonationType: "",
    startDate: "",
    finishDate: "",
    annotation: "",
    donationTypes: [],
    donationType: "",
  };
  const [errors, setErrors] = useState({});
  const [selectedRequest, setSelectedRequest] = useState(null);
  const [form, setFormState] = useState({
    cities: [],
    ...INITIAL_STATE,
  });

  // Şehir değiştiğinde ilçeler için istek at
  const handleCityChange = async (e) => {
    const { value } = e.target;

    // İlçeler için istek at
    const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/api/districts/${value}`);
    const data = await response.json();

    setFormState((prevForm) => ({
      ...prevForm,
      city: value, // Şehri güncelle
      district: "", // İlçe seçimini sıfırla
      districts: data, // İlçeleri güncelle
      neighborhoods: [], // Mahalleleri sıfırla
      neighborhood: "", // Mahalleyi sıfırla
    }));
  };

  // İlçe değiştiğinde mahalleler için istek at
  const handleDistrictChange = async (e) => {
    const { value } = e.target;

    // Mahalleler için istek at
    const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/api/neighborhoods/${value}`);
    const data = await response.json();

    setFormState((prevForm) => ({
      ...prevForm,
      district: value, // İlçeyi güncelle
      neighborhood: "", // Mahalleyi sıfırla
      neighborhoods: data, // Mahalleleri güncelle
    }));
  };

  // Mahalle değiştiğinde sadece mahalleyi güncelle
  const handleNeighborhoodChange = (e) => {
    const { value } = e.target;

    setFormState((prevForm) => ({
      ...prevForm,
      neighborhood: value, // Mahalleyi güncelle
    }));
  };

  // Şehirler için veri çekme
  useEffect(() => {
    const fetchCities = async () => {
      const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/api/cities`);
      const data = await response.json();
      setFormState((prevForm) => ({
        ...prevForm,
        cities: data, // Şehir verilerini koru
      }));
    };

    fetchCities();
  }, []);

  // Kan grupları için veri çekme
  useEffect(() => {
    const fetchBloodTypes = async () => {
      const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/api/blood-types`);
      const data = await response.json();
      setFormState((prevForm) => ({
        ...prevForm,
        bloodTypes: data, // Kan gruplarını güncelle
      }));
    };

    fetchBloodTypes();
  }, []);

  useEffect(() => {
    const donation_type = async () => {
      
      const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/api/donation_type`);
      const data = await response.json();
      setFormState((prevForm) => ({
        ...prevForm,
        donationTypes: data, // Kan gruplarını güncelle
      }));
    };

    donation_type();
  }, []);

  // Formu temizle fonksiyonu
  const clearForm = () => {
    setFormState((prevForm) => ({
      ...prevForm,
      city: "",
      district: "",
      districts: [],
      neighborhood: "",
      neighborhoods: [],
      hospital: "",
      blood_type_id: "",
      annotation: "",
      startDate: "",
      finishDate: "",
      urgency_status: "",
      donationType: "",
    }));
    setSelectedRequest(null);
  };

  // Talep oluştur butonuna basıldığında seçilen verileri ekrana yazdır
  const handleCreateRequest = async (e) => {
    e.preventDefault();
    const requestData = {
      neighborhood: form.neighborhood,
      hospital: form.hospital,
      blood_type_id: form.blood_type_id,
      urgency_status: form.urgency_status,
      annotation: form.annotation,
      startDate: form.startDate,
      finishDate: form.finishDate,
      donationType: form.donationType,
      email: email
    };
  
    try {
      console.log('Request requestData :', requestData);
      const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/create-request`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData),
      });
      
      console.log('response requestData :', response);

      if (!response.ok) throw new Error('Failed to create request');
      const result = await response.json();
      console.log('Request created successfully:', result);
      navigate("/", { state: { email: email } });
    } catch (error) {
      console.error('Error creating request:', error);
    }
  };
  
  // const handleCreateRequest = (e) => {
  //   e.preventDefault();
  //   const requestData = {
  //     //   city: form.city,
  //     //   district: form.district,
  //     neighborhood: form.neighborhood,
  //     hospital: form.hospital,
  //     bloodType: form.bloodType,
  //     demandStatus: form.demandStatus,
  //     // bloodDonationType: form.bloodDonationType,
  //     annotation: form.annotation,
  //     startDate: form.startDate,
  //     finishDate: form.finishDate,
  //     donationType: form.donationType,
  //   };

  //   setSelectedRequest(requestData);
  // };

  return (
    <>
      
      <form onSubmit={handleCreateRequest}>
        <div className="columns">
          {/* Şehir seçimi */}
          <div className="field column">
            <label className="label">İL</label>
            <div className="control select" style={{ width: "100%" }}>
              <select
                value={form.city}
                onChange={handleCityChange} // Handle city change separately
                className="select"
                name="city"
                required
                style={{ width: "100%" }}
              >
                <option value="">Seçiniz</option>
                {form.cities.map((cityItem) => (
                  <option key={cityItem.id} value={cityItem.id}>
                    {cityItem.name}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* İlçe seçimi */}
          <div className="field column">
            <label className="label">İLÇE</label>
            <div className="control select" style={{ width: "100%" }}>
              <select
                value={form.district}
                onChange={handleDistrictChange} // Handle district change separately
                className="select"
                name="district"
                required
                style={{ width: "100%" }}
              >
                <option value="">Seçiniz</option>
                {form.districts.map((districtItem) => (
                  <option key={districtItem.id} value={districtItem.id}>
                    {districtItem.name}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>

        <div className="columns">
          {/* Mahalle seçimi */}
          <div className="field column">
            <label className="label">MAHALLE</label>
            <div className="control select" style={{ width: "100%" }}>
              <select
                value={form.neighborhood}
                name="neighborhood"
                onChange={handleNeighborhoodChange} // Handle neighborhood change separately
                className="select"
                required
                style={{ width: "100%" }}
              >
                <option value="">Mahalle seçiniz</option>
                {form.neighborhoods.map((neighborhoodItem) => (
                  <option key={neighborhoodItem.id} value={neighborhoodItem.id}>
                    {neighborhoodItem.name}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Kan Bağış Merkezi / Hastane */}
          <div className="field column">
            <label className="label">KAN BAĞIŞ MERKEZİ / HASTANE</label>
            <div className="control">
              <input
                type="text"
                placeholder="bağış merkezi giriniz"
                value={form.hospital}
                onChange={(e) =>
                  setFormState((prevForm) => ({
                    ...prevForm,
                    hospital: e.target.value,
                  }))
                }
                className="input"
              />
            </div>
          </div>
        </div>

        <div className="columns">
          {/* Kan Grubu */}
          <div className="field column">
            <label className="label">TALEP EDİLEN KAN GRUBU</label>
            <div className="control select" style={{ width: "100%" }}>
              <select
                style={{ width: "100%" }}
                value={form.blood_type_id}
                onChange={(e) => {
                  setFormState((prevForm) => ({
                    ...prevForm,
                    blood_type_id: e.target.value,
                  }));
                }}
                className="select"
                required
              >
                <option value="">Kan grubu seçiniz</option>
                {form.bloodTypes.map((blood) => (
                  <option key={blood.id} value={blood.id}>
                    {blood.name}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="field column">
            <label className="label">TALEP DURUMU</label>
            <div className="control select" style={{ width: "100%" }}>
              <select
                style={{ width: "100%" }}
                value={form.urgency_status}
                onChange={(e) => {
                  setFormState((prevForm) => ({
                    ...prevForm,
                    urgency_status: e.target.value,
                  }));
                }}
                className="select"
                required
              >
                <option value="">Talep durumu seçiniz</option>
                <option value="Acil">Acil</option>
                <option value="Süreli">Süreli tarih giriniz</option>
              </select>
            </div>
          </div>
        </div>
        {form.urgency_status === "Süreli" && (
          <div className="columns">
            <div className="field column">
              <label className="label">BAŞLANGIÇ TARİHİ</label>
              <div className="control">
                <input
                  type="date"
                  value={form.startDate}
                  onChange={(e) => {
                    setFormState((prevForm) => ({
                      ...prevForm,
                      startDate: e.target.value,
                    }));
                  }}
                  className="input"
                />
              </div>
            </div>
            <div className="field column">
              <label className="label">BİTİŞ TARİHİ</label>
              <div className="control">
                <input
                  type="date"
                  value={form.finishDate}
                  onChange={(e) => {
                    setFormState((prevForm) => ({
                      ...prevForm,
                      finishDate: e.target.value,
                    }));
                  }}
                  className="input"
                />
              </div>
            </div>
          </div>
        )}
        <div className="columns">
          <div className="field column">
            <label className="label">KAN BAĞIŞ TÜRÜ</label>
            <div className="control select" style={{ width: "100%" }}>
              <select
                style={{ width: "100%" }}
                value={form.donationType}
                onChange={(e) => {
                  setFormState((prevForm) => ({
                    ...prevForm,
                    donationType: e.target.value,
                  }));
                }}
                className="select"
                required
              >
                <option value="">Kan bağış türü</option>
                {form.donationTypes.map((item) => (
                  <option key={item.id} value={item.name}>
                    {item.name}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>
        <div className="columns">
          <div className="field column">
            <label className="label">EK AÇIKLAMA</label>
            <textarea
              className="textarea"
              value={form.annotation}
              onChange={(e) => {
                setFormState((prevForm) => ({
                  ...prevForm,
                  annotation: e.target.value,
                }));
              }}
            ></textarea>
          </div>
        </div>
        {/* Formu temizle */}
        <div className="control" style={{ marginTop: "15px" }}>
          <button
            onClick={clearForm}
            type="button"
            className="button is-info is-light"
          >
            Formu Temizle
          </button>
          <button type="submit" className="button is-primary mx-3">
            Talep Oluştur
          </button>

          <button
    onClick={() => window.history.back()} // Tarayıcıda bir önceki sayfaya gider
    type="button"
    className="button is-warning is-light"
  >
    Geri Dön
  </button>
        </div>
      </form>

      {/* Ekrana yazdır */}
      {selectedRequest && (
        <div>
          <h3>Seçilen Talep:</h3>
          <pre>{JSON.stringify(selectedRequest, null, 2)}</pre>
        </div>
      )}
    </>
  );
};

export default AdsComponent;
