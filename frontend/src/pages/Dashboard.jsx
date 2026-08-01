import { useEffect, useState } from "react";

import DashboardLayout from "../layouts/DashboardLayout";
import StatCard from "../components/StatCard";
import TicketsChart from "../components/TicketsChart";
import SentimentChart from "../components/SentimentChart";
import CategoryChart from "../components/CategoryChart";
import RecentTickets from "../components/RecentTickets";
import ModelPerformance from "../components/ModelPerformance";
import SystemHealth from "../components/SystemHealth";

import { getTickets } from "../services/api";

function Dashboard() {
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadTickets() {
      try {
        const data = await getTickets();

        // Adjust later if backend response structure differs
        setTickets(data.items || data.tickets || []);
      } catch (error) {
        console.error("Failed to fetch tickets:", error);
      } finally {
        setLoading(false);
      }
    }

    loadTickets();
  }, []);

  if (loading) {
    return (
      <div
        style={{
          padding: "50px",
          fontSize: "24px",
          fontWeight: "bold",
        }}
      >
        Loading Dashboard...
      </div>
    );
  }

  const totalTickets = tickets.length;

  const openTickets = tickets.filter(
    (ticket) => ticket.status === "open"
  ).length;

  const resolvedTickets = tickets.filter(
    (ticket) =>
      ticket.status === "resolved" ||
      ticket.status === "closed"
  ).length;

  const highPriorityTickets = tickets.filter(
    (ticket) =>
      ticket.priority === "high" ||
      ticket.priority === "urgent" ||
      ticket?.prediction?.priority === "high" ||
      ticket?.prediction?.priority === "urgent"
  ).length;

  return (
    <DashboardLayout>
      

        <div
          style={{
            padding: "25px",
            display: "grid",
            gridTemplateColumns:
              "repeat(auto-fit,minmax(220px,1fr))",
            gap: "20px",
          }}
        >
          <StatCard
            title="Total Tickets"
            value={totalTickets}
            color="#7c3aed"
          />

          <StatCard
            title="Open Tickets"
            value={openTickets}
            color="#22c55e"
          />

          <StatCard
            title="High Priority"
            value={highPriorityTickets}
            color="#f59e0b"
          />

          <StatCard
            title="Resolved"
            value={resolvedTickets}
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
            gap: "20px",
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
            gap: "20px",
          }}
        >
          <RecentTickets />
          <ModelPerformance />
          <SystemHealth />
        </div>
      </DashboardLayout>
  );
  
}

export default Dashboard;