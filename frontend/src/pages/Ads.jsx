import React from "react";
import AdsComponent from "../components/AdsComponent";
const Ads = () => {
  return (
    <div className="container my-4">
      <p style={{ textAlign: "center", fontSize: "25px" }}>
        <strong>İlan Olustur</strong>
      </p>
      <br />
      <AdsComponent />
    </div>
  );
};

export default Ads;
