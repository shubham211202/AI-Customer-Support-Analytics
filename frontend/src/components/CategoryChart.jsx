import { PieChart, Pie, Cell, ResponsiveContainer } from "recharts";

const data = [
  { name: "Billing", value: 25 },
  { name: "Technical", value: 22 },
  { name: "Account", value: 18 },
  { name: "Shipping", value: 15 },
  { name: "Other", value: 20 }
];

const COLORS = [
  "#3b82f6",
  "#8b5cf6",
  "#22c55e",
  "#f59e0b",
  "#94a3b8"
];

function CategoryChart() {
  return (
    <div
      style={{
        background: "white",
        borderRadius: "15px",
        padding: "20px",
        height: "400px"
      }}
    >
      <h3>Ticket Categories</h3>

      <ResponsiveContainer width="100%" height="90%">
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

export default CategoryChart;