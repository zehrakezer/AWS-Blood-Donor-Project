import React, { useContext } from "react";
import { useLocation } from "react-router-dom";
import { UserContext } from "../context/UserContext";

const Header = ({ title }) => {
  const [token, setToken] = useContext(UserContext);

  const handleLogout = () => {
    setToken(null);
  };

  const location = useLocation();
  const email = location.state?.email; 
  console.log("Header Who are u?", email)

  return (
    <div className="has-text-centered m-6">
      <h1 className="title">{title}</h1>
      {token && (
        <button className="button" onClick={handleLogout}>
          Çıkış Yap
        </button>
      )}
    </div>
  );
};

export default Header;
