import React from "react";

function ListofPlayers() {

    const players = [
        { name: "Virat Kohli", score: 95 },
        { name: "Rohit Sharma", score: 85 },
        { name: "Shubman Gill", score: 78 },
        { name: "KL Rahul", score: 65 },
        { name: "Hardik Pandya", score: 72 },
        { name: "Ravindra Jadeja", score: 68 },
        { name: "R Ashwin", score: 55 },
        { name: "Jasprit Bumrah", score: 80 },
        { name: "Mohammed Shami", score: 62 },
        { name: "Mohammed Siraj", score: 58 },
        { name: "Kuldeep Yadav", score: 74 }
    ];

    const lowScorePlayers = players.filter(player => player.score < 70);

    return (
        <div>

            <h2>List of Players</h2>

            <ul>
                {
                    players.map((player, index) => (
                        <li key={index}>
                            {player.name} - {player.score}
                        </li>
                    ))
                }
            </ul>

            <h2>Players with Scores Below 70</h2>

            <ul>
                {
                    lowScorePlayers.map((player, index) => (
                        <li key={index}>
                            {player.name} - {player.score}
                        </li>
                    ))
                }
            </ul>

        </div>
    );
}

export default ListofPlayers;