import axios from "axios";

export const apiClient = axios.create({
  baseURL: "/api"
});

export function planTrip(payload: Record<string, unknown>) {
  return apiClient.post("/plan-trip", payload);
}

export function customizeTrip(payload: Record<string, unknown>) {
  return apiClient.post("/customize-trip", payload);
}

export function fetchEvents(params: Record<string, string>) {
  return apiClient.get("/events", { params });
}

export function fetchWeather(params: Record<string, string>) {
  return apiClient.get("/weather", { params });
}

export function sendChatMessage(payload: Record<string, unknown>) {
  return apiClient.post("/chat", payload);
}

export function saveTrip(payload: Record<string, unknown>) {
  return apiClient.post("/save", payload);
}
