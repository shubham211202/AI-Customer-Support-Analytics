import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid
} from "recharts";

const data = [
  { day: "Mon", total: 1100, resolved: 500 },
  { day: "Tue", total: 1600, resolved: 900 },
  { day: "Wed", total: 1250, resolved: 550 },
  { day: "Thu", total: 1750, resolved: 950 },
  { day: "Fri", total: 1900, resolved: 1050 },
  { day: "Sat", total: 1500, resolved: 850 },
  { day: "Sun", total: 2000, resolved: 1400 }
];

function TicketsChart() {
  return (
    <div
      style={{
        background: "white",
        borderRadius: "15px",
        padding: "20px",
        boxShadow: "0 2px 8px rgba(0,0,0,0.05)"
      }}
    >
      <h3 style={{ marginBottom: "20px" }}>
        Tickets Over Time
      </h3>

      <ResponsiveContainer width="100%" height={350}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />

          <XAxis dataKey="day" />
          <YAxis />

          <Tooltip />

          <Line
            type="monotone"
            dataKey="total"
            stroke="#7c3aed"
            strokeWidth={3}
          />

          <Line
            type="monotone"
            dataKey="resolved"
            stroke="#22c55e"
            strokeWidth={3}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export default TicketsChart;