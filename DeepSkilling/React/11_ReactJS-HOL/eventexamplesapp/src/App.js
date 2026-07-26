import React, { useState } from "react";

import "./App.css";

import CurrencyConvertor from "./components/CurrencyConvertor";

function App() {

    const [count, setCount] = useState(0);

    const increment = () => {

        setCount(count + 1);

    };

    const decrement = () => {

        setCount(count - 1);

    };

    const sayHello = () => {

        alert("Hello! Member!");

    };

    const increase = () => {

        increment();

        sayHello();

    };

    const sayWelcome = (message) => {

        alert(message);

    };

    const syntheticEvent = () => {

        alert("I was clicked");

    };

    return (

        <div className="container">

            <p>{count}</p>

            <button onClick={increase}>

                Increment

            </button>

            <br />

            <button onClick={decrement}>

                Decrement

            </button>

            <br />

            <button onClick={() => sayWelcome("welcome")}>

                Say welcome

            </button>

            <br />

            <button onClick={syntheticEvent}>

                Click on me

            </button>

            <br />

            <CurrencyConvertor />

        </div>

    );

}

export default App;