import React, { useContext, useEffect, useState } from "react";
import moment from "moment";
import Header from "./Header";
import ErrorMessage from "./ErrorMessage";
import LeadModal from "./LeadModal";
import { UserContext } from "../context/UserContext";
import { useNavigate } from "react-router-dom";
import { useLocation } from "react-router-dom";



console.log("in Table Base URL:", process.env.REACT_APP_API_BASE_URL);

const Table = () => {
  const location = useLocation();
  const email = location.state?.email;
  console.log("Table-Dash Who are u?", email);
  const navigate = useNavigate(); // Initialize the navigate function
  const [token] = useContext(UserContext);
  const [data, setData] = useState([]); // Verileri saklar
  const [loaded, setLoaded] = useState(false); // Yükleme durumu
  const [errorMessage, setErrorMessage] = useState("");
  const [isSelf, setIsSelf] = useState(false);
  const [activeButton, setActiveButton] = useState("none"); // Yeni durum
  const [activeButton2, setActiveButton2] = useState("none"); // new
  const [isSil, setIsSil] = useState(false);


  // Veriyi fetch eden fonksiyon
  const fetchData = async () => {
    setIsSelf(false);
    setIsSil(true);
    setActiveButton("other"); // Diğer ilanlar butonunu aktif yap
    setActiveButton2("other"); // sil butonu none
    try {
      const requestOptions = {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + token,
        },
      };
      const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/other-blood-donation-publications/${email}`, requestOptions);
      if (!response.ok) {
        throw new Error("Something went wrong. Couldn't load the data.");
      }
      const responseData = await response.json();
      setData(responseData); // Veriyi kaydet
      setLoaded(true);
    } catch (error) {
      console.error("Error fetching data:", error);
      setErrorMessage("Failed to load data");
      setLoaded(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [token]);

  const fetchData2 = async () => {
    setIsSelf(true);
    setIsSil(false);
    setActiveButton("self"); // Kendi ilanlar butonunu aktif yap
    setActiveButton2("self"); // sil butonu
    try {
      const requestOptions = {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + token,
        },
      };
      const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/self-blood-donation-publications/${email}`, requestOptions);
      if (!response.ok) {
        throw new Error("Something went wrong. Couldn't load the data.");
      }
      const responseData = await response.json();
      setData(responseData); // Veriyi kaydet
      setLoaded(true);
    } catch (error) {
      console.error("Error fetching data:", error);
      setErrorMessage("Failed to load data");
      setLoaded(false);
    }
  };

  const updateDonation = async (user_id, location) => {
    setIsSelf(true);
    try {
      const requestOptions = {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + token,
        },
      };
      const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/apply-publications/${user_id}/${email}/${location}`, requestOptions);
      if (!response.ok) {
        throw new Error("Something went wrong. Couldn't load the data.");
      }
      alert("İşlem Başarılı. Teşekkürler.");
      fetchData2();
    } catch (error) {
      console.error("Error fetching data:", error);
      setErrorMessage("Failed to load data");
    }
    setLoaded(false);
  };

  const deletePub = async (user_id, location) => {
    setIsSelf(true);
    try {
      const requestOptions = {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + token,
        },
      };
      const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/delete-publications/${user_id}/${email}/${location}`, requestOptions);
      if (!response.ok) {
        throw new Error("Something went wrong. Couldn't load the data.");
      }
      alert("İşlem Başarılı. Teşekkürler.");
      fetchData2();
    } catch (error) {
      console.error("Error fetching data:", error);
      setErrorMessage("Failed to load data");
    }
    setLoaded(false);
  };


  const handleUpdate = (id) => {
    console.log("Update clicked for ID:", id);
    // Update işlemi burada yapılabilir
  };

  const handleDelete = async (id) => {
    try {
      const requestOptions = {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + token,
        },
      };
      const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/blood-donation-publications/${id}`, requestOptions);
      if (!response.ok) {
        throw new Error("Failed to delete data");
      }
      setData((prevData) => prevData.filter((record) => record.id !== id));
    } catch (error) {
      console.error("Delete failed:", error);
      setErrorMessage("Failed to delete record");
    }
  };

  const getDonationTypeText = (donationType) => {
    switch (donationType) {
      case 1:
        return "Tam Kan Bağışı";
      case 2:
        return "Tromboferez";
      case 3:
        return "Eritroferez";
      case 4:
        return "Plazmaferez";
      default:
        return "Bilinmiyor";
    }
  };

  const Urgency = (donationType) => {
    switch (donationType) {
      case 1:
        return "Acil";
      case 2:
        return "Süreli";
    }
  };

  const bloodTypeText = (donationType) => {
    switch (donationType) {
      case 1:
        return "A Rh +";
      case 2:
        return "A Rh -";
      case 3:
        return "B Rh +";
      case 4:
        return "B Rh -";
      case 5:
        return "0 Rh +";
      case 8:
        return "0 Rh -";
      case 6:
        return "AB Rh +";
      case 7:
        return "AB Rh -";
      default:
        return "Bilinmiyor";
    }
  };

  return (
    <>
      <LeadModal
        active={false}
        handleModal={() => {}}
        token={token}
        id={null}
        setErrorMessage={setErrorMessage}
      />
      <Header title="Kan Bağış Sistemi" />
      <h1>İlan Yönetim ve Başvuru Listeleriniz</h1>
      <br />
      
      <ErrorMessage message={errorMessage} />

      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          gap: "10px", // Butonlar arasında boşluk bırakır
        }}
      >
        <button
          className="button is-primary"
          style={{ flex: "1" }} // Butonların eşit genişlikte olmasını sağlar
          onClick={() => navigate("/createPublication", { state: { email } })}
        >
          Yeni Kan Arama İlanı Aç
        </button>

        <button
          style={{
            flex: "1",
            backgroundColor: "#209CEE",
            color: "white",
            border: activeButton === "self" ? "2px solid #000000" : "none",
          }}
          className="button"
          onClick={() => fetchData2()}
        >
          Sahibi Olduğum İlanlar
        </button>

  <button
    style={{
      flex: "1",
      backgroundColor: "#209CEE",
      color: "white",
      border: activeButton === "other" ? "2px solid #000000" : "none",
    }}
    className="button"
    onClick={() => fetchData()}
  >
    Diğer İlanlar
  </button>
</div>



      {loaded && data.length > 0 ? (
        <table className="table is-fullwidth">
          <thead>
            <tr>
             
              <th>Tarih</th>
              <th>Aciliyet</th>
              <th>Bağış Türü</th>
              <th>Aranan Kan Türü</th>
              <th>Lokasyon</th>
              <th>Bağış Yeri</th>
              <th>İlani Açanın Bilgisi</th>
              <th>İlana Başvuranın Bilgisi</th>
              <th>Ek Açıklama</th>
              <th>Durum</th>
              {!isSelf && <th>Actions</th>}
              {!isSil && <th>Actions</th>}
            </tr>
          </thead>
          <tbody>
            {data.map((record) => (
              <tr key={record.id}>
               
                <td>
                  {record.start_date
                    ? moment(record.created_date).format("YYYY-MM-DD")
                    : "--"}
                </td>
                <td>{Urgency(record.urgency_status)}</td>
                <td>{getDonationTypeText(record.donation_type)}</td>
                <td>{bloodTypeText(record.blood_type_id)}</td>
                <td>{record.location2}</td>
                <td>{record.hospital_name}</td>
                <td>{record.opener}</td>
                <td>{record.applied}</td>
                <td>{record.description || "--"}</td>
                <td>
                  {record.status === 1
                    ? "Başarılı"
                    : record.status === 2
                    ? "Başarısız"
                    : "Devam Eden"}
                </td>
                {!isSelf && (
                  <td>
                    <button
                      className="button mr-2 is-info is-light"
                      onClick={() => updateDonation(record.user_id, record.location)}
                    >
                      Bağışçı Ol
                    </button>
                  </td>
                )}
                {!isSil && (
                  <td>
                    <button
                      className="button mr-2 is-info is-light"
                      onClick={() => deletePub(record.user_id, record.location)}
                    >
                      İlanı Sil
                    </button>
                  </td>
                )}
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>Siz de ilan oluşturabilirsiniz...</p>
      )}
    </>
  );
};

export default Table;
