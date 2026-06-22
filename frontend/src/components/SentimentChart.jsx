import { PieChart, Pie, Cell, ResponsiveContainer } from "recharts";

const data = [
  { name: "Positive", value: 45 },
  { name: "Neutral", value: 25 },
  { name: "Negative", value: 30 }
];

const COLORS = ["#22c55e", "#f59e0b", "#ef4444"];

function SentimentChart() {
  return (
    <div
      style={{
        background: "white",
        borderRadius: "15px",
        padding: "20px",
        height: "350px"
      }}
    >
      <h3>Sentiment Analysis</h3>

      <ResponsiveContainer width="100%" height={250}>
        <PieChart>
          <Pie
            data={data}
            innerRadius={70}
            outerRadius={100}
            dataKey="value"
          >
            {data.map((entry, index) => (
              <Cell
                key={index}
                fill={COLORS[index]}
              />
            ))}
          </Pie>
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}

export default SentimentChart;