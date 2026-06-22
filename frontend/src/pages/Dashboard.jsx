import Sidebar from "../components/Sidebar";
import Header from "../components/Header";
import StatCard from "../components/StatCard";
import TicketsChart from "../components/TicketsChart";
import SentimentChart from "../components/SentimentChart";
import CategoryChart from "../components/CategoryChart";
import RecentTickets from "../components/RecentTickets";
import ModelPerformance from "../components/ModelPerformance";
import SystemHealth from "../components/SystemHealth";

function Dashboard() {
  return (
    <>
      <Sidebar />

      <div
        style={{
          marginLeft: "260px",
          minHeight: "100vh"
        }}
      >
        <Header />

        <div
          style={{
            padding: "25px",
            display: "grid",
            gridTemplateColumns:
              "repeat(auto-fit,minmax(220px,1fr))",
            gap: "20px"
          }}
        >
          <StatCard
            title="Total Tickets"
            value="12,543"
            color="#7c3aed"
          />

          <StatCard
            title="Open Tickets"
            value="3,382"
            color="#22c55e"
          />

          <StatCard
            title="High Priority"
            value="482"
            color="#f59e0b"
          />

          <StatCard
            title="Resolved"
            value="9,161"
            color="#2563eb"
          />

          <StatCard
            title="Avg Response"
            value="2.45 hrs"
            color="#ef4444"
          />
        </div>
        
      <div
  style={{
    padding: "0 25px 25px",
    display: "grid",
    gridTemplateColumns: "2fr 1fr 1fr",
    gap: "20px"
  }}
>
  <TicketsChart />
  <SentimentChart />
  <CategoryChart />
</div>  
<div
  style={{
    padding: "0 25px 25px",
    display: "grid",
    gridTemplateColumns: "2fr 1fr",
    gap: "20px"
  }}
>
  <RecentTickets />
  <ModelPerformance />
  <SystemHealth />
</div>

      </div>
    </>
  );
}

export default Dashboard;