import React, { useState } from "react";

function CurrencyConvertor() {

    const [amount, setAmount] = useState("");
    const [currency, setCurrency] = useState("");

    const handleSubmit = (event) => {

        event.preventDefault();

        const euroAmount = amount * 80;

        alert("Converting to Euro Amount is " + euroAmount);

    };

    return (

        <div className="converter">

            <h1>Currency Convertor!!!</h1>

            <form onSubmit={handleSubmit}>

                <table>

                    <tbody>

                        <tr>

                            <td>Amount:</td>

                            <td>

                                <input
                                    type="number"
                                    value={amount}
                                    onChange={(e) => setAmount(e.target.value)}
                                />

                            </td>

                        </tr>

                        <tr>

                            <td>Currency:</td>

                            <td>

                                <input
                                    type="text"
                                    value={currency}
                                    onChange={(e) => setCurrency(e.target.value)}
                                />

                            </td>

                        </tr>

                        <tr>

                            <td></td>

                            <td>

                                <button type="submit">

                                    Submit

                                </button>

                            </td>

                        </tr>

                    </tbody>

                </table>

            </form>

        </div>

    );

}

export default CurrencyConvertor;