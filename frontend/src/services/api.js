import axios from "axios";

// Backend API Base URL
const API = axios.create({
  baseURL: "http://127.0.0.1:8000/api/v1",
  headers: {
    "Content-Type": "application/json",
  },
});

// Automatically attach JWT token to every request
API.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("accessToken");

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => Promise.reject(error)
);

// ==========================
// Authentication APIs
// ==========================

export const login = async (email, password) => {
  const formData = new URLSearchParams();

  formData.append("username", email);
  formData.append("password", password);

  const response = await API.post(
    "/auth/login",
    formData,
    {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    }
  );

  return response.data;
};

export const register = async (userData) => {
  const response = await API.post("/auth/register", userData);
  return response.data;
};

// ==========================
// Ticket APIs
// ==========================

export const getTickets = async () => {
  const response = await API.get("/tickets");
  return response.data;
};

export const createTicket = async (ticketData) => {
  const response = await API.post("/tickets", ticketData);
  return response.data;
};

export const updateTicketStatus = async (ticketId, status) => {
  const response = await API.patch(
    `/tickets/${ticketId}/status`,
    { status }
  );

  return response.data;
};

export const deleteTicket = async (ticketId) => {
  await API.delete(`/tickets/${ticketId}`);
};

export default API;