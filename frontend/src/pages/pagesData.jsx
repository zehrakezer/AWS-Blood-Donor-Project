import Home from "./Home";
import Login from "./LoginPage";
import RegisterPage from "./RegisterPage";
import Ads from "./Ads";
import React from "react";

const pagesData = [
  {
    path: "/",
    element: <Home />,
    title: "Anasayfa",
  },
  {
    path: "/login",
    element: <Login />,
    title: "Login Page",
  },
  {
    path: "/register",
    element: <RegisterPage />,
    title: "Register Page",
  },
  {
    path: "/createPublication",
    element: <Ads />,
    title: "createPublication",
  },
];

export default pagesData;
