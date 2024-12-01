import React, { useState, useEffect, useContext } from "react";
import Login from "../components/Login";
import { UserContext } from "../context/UserContext";
import Table from "../components/Table";
import { useLocation } from "react-router-dom";

const Home = () => {
  const location = useLocation();
  const email = location.state?.email; 
  console.log("Home Who are u?", email)
  const [message, setMessage] = useState("");
  const [token] = useContext(UserContext);

  const getWelcomeMessage = async () => {
    const requestOptions = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    };
    const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/api`, requestOptions);
    const data = await response.json();

    if (!response.ok) {
      console.log("something messed up");
    } else {
      setMessage(data.message);
    }
  };

  useEffect(() => {
    getWelcomeMessage();
  }, []);
  return (
    <>
      {/* <Header title={message} />
      <div
        className="is-flex is-justify-content-center"
        style={{ gap: "20px" }}
      >
        <button className="button">
          <Link to="/register">Register</Link>
        </button>
        <button className="button is-link">
          <Link to="/login" style={{ color: "white" }}>
            Login
          </Link>
        </button>
      </div> */}
      <div className="container">
        {/* <Login /> */}
        {!token ? (
          <>
            <Login />
          </>
        ) : (
          <Table />
        )}
      </div>
      {/* <div className="columns">
        <div className="column"></div>
        <div className="column m-5 is-two-thirds">
          {
            !token ? (
              <div className="columns">
                <Register /> <Login />
              </div>
            )
              : (
                <Table />
              )
          }
        </div>
        <div className="column"></div>
      </div> */}
    </>
  );
};

export default Home;
