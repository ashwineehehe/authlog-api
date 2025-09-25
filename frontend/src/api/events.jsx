import api from "./axios"; // baseURL http://127.0.0.1:8000/api/v1

// GET all (with query params: limit, offset, outcome)
export const listEvents = (params = {}) =>
  api.get("/events", { params });

// GET one by ID
export const getEvent = (id) =>
  api.get(`/events/${id}`);

// POST create new event
export const createEvent = (data) =>
  api.post("/events", data);

// PUT full replace existing event
export const replaceEvent = (id, data) =>
  api.put(`/events/${id}`, data);

// PATCH partial update existing event
export const patchEvent = (id, data) =>
  api.patch(`/events/${id}`, data);

// DELETE one by ID
export const deleteEvent = (id) =>
  api.delete(`/events/${id}`);
