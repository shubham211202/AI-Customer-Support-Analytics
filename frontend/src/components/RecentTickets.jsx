function RecentTickets() {
  const tickets = [
    {
      id: "#TKT-10125",
      title: "Unable to login account",
      status: "Open"
    },
    {
      id: "#TKT-10124",
      title: "Payment gateway issue",
      status: "Resolved"
    },
    {
      id: "#TKT-10123",
      title: "Invoice not received",
      status: "In Progress"
    }
  ];

  return (
    <div
      style={{
        background: "white",
        borderRadius: "15px",
        padding: "20px"
      }}
    >
      <h3>Recent Tickets</h3>

      {tickets.map((ticket) => (
        <div
          key={ticket.id}
          style={{
            padding: "15px 0",
            borderBottom: "1px solid #eee"
          }}
        >
          <strong>{ticket.id}</strong>

          <p>{ticket.title}</p>

          <span>{ticket.status}</span>
        </div>
      ))}
    </div>
  );
}

export default RecentTickets;