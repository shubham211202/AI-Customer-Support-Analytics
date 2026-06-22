import {
  FaChartPie,
  FaTicketAlt,
  FaRobot,
  FaUsers,
  FaBell,
  FaCog
} from "react-icons/fa";

function Sidebar() {
  return (
    <div
      style={{
        width: "260px",
        height: "100vh",
        background: "#0B1120",
        color: "white",
        padding: "20px",
        position: "fixed"
      }}
    >
      <h2 style={{ marginBottom: "40px" }}>
        AI Support Analytics
      </h2>

      <div style={{ display: "flex", flexDirection: "column", gap: "25px" }}>
        <div><FaChartPie /> Dashboard</div>
        <div><FaTicketAlt /> Tickets</div>
        <div><FaRobot /> AI Predictions</div>
        <div><FaUsers /> Customers</div>
        <div><FaBell /> Alerts</div>
        <div><FaCog /> Settings</div>
      </div>
    </div>
  );
}

export default Sidebar;