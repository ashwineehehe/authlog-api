import api from "./axios";

export const registerUser = (email, password) =>
  api.post("/users", { email, password });

export const loginUser = (email, password) =>
  api.post("/users/login", { email, password });

// For OAuth2PasswordRequestForm (username= email, password)
export const login = (email, password) =>
  api.post("/users/login", new URLSearchParams({ username: email, password }));

export const register = (email, password) =>
  api.post("/users", { email, password });
