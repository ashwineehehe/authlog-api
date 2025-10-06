import React from "react";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import UsersPage from "./pages/UsersPage";
import EventsPage from "./pages/EventsPage";

function App() {
  return (
    <BrowserRouter>
      <nav style={{ display: "flex", gap: "12px", padding: "12px" }}>
        <Link to="/">Users</Link>
        <Link to="/events">Events</Link>
      </nav>
      <Routes>
        <Route path="/" element={<UsersPage />} />
        <Route path="/events" element={<EventsPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
