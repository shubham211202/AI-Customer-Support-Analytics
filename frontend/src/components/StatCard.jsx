function StatCard({ title, value, color }) {
  return (
    <div
      style={{
        background: "white",
        borderRadius: "15px",
        padding: "25px",
        minWidth: "220px",
        boxShadow: "0 2px 8px rgba(0,0,0,0.05)"
      }}
    >
      <p style={{ color }}>{title}</p>

      <h1
        style={{
          marginTop: "10px",
          fontSize: "32px"
        }}
      >
        {value}
      </h1>
    </div>
  );
}

export default StatCard;