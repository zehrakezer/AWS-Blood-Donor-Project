import React, { useState, useContext } from "react";

import ErrorMessage from "./ErrorMessage";
import { UserContext } from "../context/UserContext";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";

const Login = () => {
  const navigate = useNavigate(); // useNavigate hook
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [, setToken] = useContext(UserContext);

  const submitLogin = async () => {
    console.log("Base URL:", process.env.REACT_APP_API_BASE_URL);

    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: JSON.stringify(
        `grant_type=&username=${email}&password=${password}`
      ),
    };
    // &scope=&client_id=&client_secret=

    const response = await fetch(
      `${process.env.REACT_APP_API_BASE_URL}/api/token`,
      requestOptions
    );
    const data = await response.json();

    if (!response.ok) {
      setErrorMessage(data.detail);
    } else {
      setToken(data.access_token);
      console.log("Who are u?", email)
      navigate("/", { state: { email: email } });
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    submitLogin();
  };

  return (
    <div className="column">
      <form className="box" onSubmit={handleSubmit}>
        <h1 className="title has-text-centered">Kan Bağış Sistemine Hoş Geldiniz "Bir Hayat Kurtarın!"</h1>
        <div className="field">
          <label className="label">Email</label>
          <div className="control">
            <input
              type="email"
              placeholder="Mail Yazınız"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="input"
              required
            />
          </div>
        </div>
        <div className="field">
          <label className="label">Parola</label>
          <div className="control">
            <input
              type="password"
              placeholder="Parola Giriniz"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="input"
              required
            />
          </div>
        </div>
        <ErrorMessage message={errorMessage} />
        <br />
        <Link to="/register">Hesabınız yok mu ? Hemen Üye Olun</Link>
        <br />
        <br />
        <button className="button is-primary" type="submit">
          Giriş Yap
        </button>
        {/* <button className="button  mx-2">
          <Link to="/ads"> İlanlar Sayfası</Link>
        </button> */}
      </form>
    </div>
  );
};

export default Login;
