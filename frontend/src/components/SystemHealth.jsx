function HealthCard({ title }) {
  return (
    <div
      style={{
        background: "white",
        borderRadius: "12px",
        padding: "20px",
        textAlign: "center"
      }}
    >
      <h4>{title}</h4>

      <p
        style={{
          color: "#22c55e",
          marginTop: "10px"
        }}
      >
        Healthy
      </p>
    </div>
  );
}

function SystemHealth() {
  return (
    <div
      style={{
        padding: "25px"
      }}
    >
      <h2>System Health</h2>

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(auto-fit,minmax(180px,1fr))",
          gap: "20px",
          marginTop: "20px"
        }}
      >
        <HealthCard title="API Service" />
        <HealthCard title="ML Service" />
        <HealthCard title="Database" />
        <HealthCard title="Redis Cache" />
        <HealthCard title="Storage" />
        <HealthCard title="Kubernetes" />
      </div>
    </div>
  );
}

export default SystemHealth;