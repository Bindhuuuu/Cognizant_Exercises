import "../Stylesheets/mystyle.css";

const percentToDecimal = (decimal) => {
  return (decimal.toFixed(2) + "%");
};

const calcScore = (total, goal) => {
  return percentToDecimal(total / goal);
};

export function CalculateScore({ Name, School, total, goal }) {
  return (
    <div className="formatstyle">
      <h1>
        <font color="brown">Student Details:</font>
      </h1>

      <div className="Name">
        <b>Name: </b>
        <span>{Name}</span>
      </div>

      <div className="School">
        <b>School: </b>
        <span>{School}</span>
      </div>

      <div className="Total">
        <b>Total: </b>
        <span>{total} Marks</span>
      </div>

      <div className="Score">
        <b>Score: </b>
        <span>{calcScore(total, goal)}</span>
      </div>
    </div>
  );
}