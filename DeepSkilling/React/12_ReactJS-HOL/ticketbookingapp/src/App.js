import React, { useState } from "react";

import "./App.css";

import Greeting from "./components/Greeting";
import LoginButton from "./components/LoginButton";
import LogoutButton from "./components/LogoutButton";

function App() {

    const [isLoggedIn, setIsLoggedIn] = useState(false);

    const handleLogin = () => {

        setIsLoggedIn(true);

    };

    const handleLogout = () => {

        setIsLoggedIn(false);

    };

    let button;

    if (isLoggedIn) {

        button = <LogoutButton onClick={handleLogout} />;

    }

    else {

        button = <LoginButton onClick={handleLogin} />;

    }

    return (

        <div className="container">

            <Greeting isLoggedIn={isLoggedIn} />

            {button}

        </div>

    );

}

export default App;