import { FaBell, FaMoon } from "react-icons/fa";

function Header() {
  return (
    <div
      style={{
        background: "white",
        padding: "20px 30px",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        borderBottom: "1px solid #e5e7eb"
      }}
    >
      <h2>Dashboard</h2>

      <div style={{ display: "flex", gap: "20px" }}>
        <FaBell />
        <FaMoon />
      </div>
    </div>
  );
}

export default Header;