import React, { useContext, useEffect, useState } from "react";
import moment from "moment";
import Header from "./Header";
import ErrorMessage from "./ErrorMessage";
import LeadModal from "./LeadModal";
import { UserContext } from "../context/UserContext";
import { useNavigate } from "react-router-dom";
import { useLocation } from "react-router-dom";


const Table = () => {
  const location = useLocation();
  const email = location.state?.email; 
  console.log("Table-Dash Who are u?", email)
  const navigate = useNavigate(); // Initialize the navigate function
  const [token] = useContext(UserContext);
  const [data, setData] = useState([]); // Verileri saklar
  const [loaded, setLoaded] = useState(false); // Yükleme durumu
  const [errorMessage, setErrorMessage] = useState("");
  const [isSelf, setIsSelf] = useState(false); 


  // Veriyi fetch eden fonksiyon
  const fetchData = async () => {
    setIsSelf(false);
    try {
      const requestOptions = {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + token,
        },
      };
      const response = await fetch(`/other-blood-donation-publications/${email}`, requestOptions);
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
    try {
      const requestOptions = {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + token,
        },
      };
      const response = await fetch(`/self-blood-donation-publications/${email}`, requestOptions);
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

  const updateDonation = async (user_id,location) => {
    setIsSelf(true);
    try {
      const requestOptions = {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + token,
        },
      };
      const response = await fetch(`/apply-publications/${user_id}/${email}/${location}`, requestOptions);
      if (!response.ok) {
        throw new Error("Something went wrong. Couldn't load the data.");
      }
      alert("Islem Basarili. Tesekkürler.");
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
      // /${id}
      const response = await fetch(`/blood-donation-publications/${id}`, requestOptions);
      if (!response.ok) {
        throw new Error("Failed to delete data");
      }
      // Başarıyla silindikten sonra tabloyu güncelle
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
        active={false} // Modal örneği için aktif değil
        handleModal={() => {}}
        token={token}
        id={null}
        setErrorMessage={setErrorMessage}
      />
       <Header title="Exit" />
      <h1>DASHBOARD</h1>
      <br />
      <button
        className="button is-fullwidth mb-5 is-primary"
        onClick={() => navigate("/createPublication", { state: { email } })}
      >
        Ilan Gir
      </button>
      <ErrorMessage message={errorMessage} />
      <button  onClick={() => fetchData2()}
        >Kendi Ilanlarim</button>
      <button  onClick={() => fetchData()}
      >Diger Ilanlar</button>
      {loaded && data.length > 0 ? (
        <table className="table is-fullwidth">
          <thead>
            <tr>
              {/* <th>User ID</th> */}
              <th>Tarih</th>
              <th>Urgency Status</th>
              <th>Donation Type</th>
              <th>Blood Type</th>
              <th>Location</th>
              <th>Hospital Name</th>
              <th>Ilani Acan</th>
              <th>Ilana Basvuran</th>              
              
              {/* <th>Start Date</th>
              <th>End Date</th> */}
              
              <th>Description</th>
              <th>Status</th>
              {/* <th>Location</th> */}
              
             {!isSelf && <th>Actions</th>}
            </tr>
          </thead>
          <tbody>
            {data.map((record) => (
              <tr key={record.id}>
                {/* <td>{record.user_id}</td> */}
                <td>{record.start_date
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
                
                {/* <td>
                  {record.start_date
                    ? moment(record.start_date).format("YYYY-MM-DD")
                    : "--"}
                </td>
                <td>
                  {record.end_date
                    ? moment(record.end_date).format("YYYY-MM-DD")  
                    : "--"}
                </td> */}
                
                {/* <td>{record.donation_type}</td> */}
                <td>{record.description || "--"}</td>
                <td>
                  {record.status === 1
                    ? "Başarılı"
                    : record.status === 2
                    ? "Başarısız"
                    : "Devam Eden"}
                </td>
                {/* <td>{record.location}</td> */}
                
                
                {!isSelf && <td>
                  <button
                    className="button mr-2 is-info is-light"
                    onClick={() => updateDonation(record.user_id,record.location)}
                  >
                    Bagisci Ol
                  </button>
                  {/* <button
                    className="button mr-2 is-danger is-light"
                    onClick={() => handleDelete(record.id)}
                  >
                    Delete
                  </button> */}
                </td>}
              </tr>
            ))}
          </tbody>
        </table>

        
      ) : (
        <p>Siz de ilan olusturabilirsiniz...</p>
        
      )}
    </>
  );
};

export default Table;
