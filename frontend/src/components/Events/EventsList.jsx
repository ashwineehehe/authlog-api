import { useEffect, useState } from "react";
import { listEvents, deleteEvent, getEvent } from "../../api/events";
import EventForm from "./EventForm";

export default function EventsList() {
  const [events, setEvents] = useState([]);
  const [limit, setLimit] = useState(10);
  const [offset, setOffset] = useState(0);
  const [outcome, setOutcome] = useState(""); // success | failure | ""
  const [loading, setLoading] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [editingData, setEditingData] = useState(null);
  const [msg, setMsg] = useState("");

  const load = async () => {
    try {
      setLoading(true);
      const params = { limit, offset };
      if (outcome) params.outcome = outcome;
      const res = await listEvents(params);
      setEvents(res.data);
    } catch (e) {
      setMsg(e.response?.data?.detail || "Failed to fetch events");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, [limit, offset, outcome]);

  const onDelete = async (id) => {
    if (!confirm(`Delete event #${id}?`)) return;
    try {
      await deleteEvent(id);
      setMsg(`Deleted event #${id}`);
      load();
    } catch (e) {
      setMsg(e.response?.data?.detail || "Delete failed");
    }
  };

  const onEdit = async (id) => {
    try {
      const res = await getEvent(id);
      setEditingId(id);
      setEditingData(res.data);
      window.scrollTo(0, 0);
    } catch (e) {
      setMsg(e.response?.data?.detail || "Could not load event");
    }
  };

  return (
    <div>
      <h2>Events</h2>

      {/* Create / Edit form */}
      <EventForm
        key={editingId || "create"}
        initial={editingData}
        onDone={() => {
          setEditingId(null);
          setEditingData(null);
          load();
        }}
      />

      {/* Filters / pagination */}
      <div style={{ margin: "16px 0" }}>
        <label>Outcome: </label>
        <select value={outcome} onChange={(e) => setOutcome(e.target.value)}>
          <option value="">(all)</option>
          <option value="success">success</option>
          <option value="failure">failure</option>
        </select>

        <label style={{ marginLeft: 12 }}>Limit:</label>
        <input type="number" value={limit} min={1} max={200} onChange={(e) => setLimit(+e.target.value)} style={{ width: 70, marginLeft: 4 }} />

        <button onClick={() => setOffset(Math.max(0, offset - limit))} style={{ marginLeft: 12 }}>Prev</button>
        <button onClick={() => setOffset(offset + limit)} style={{ marginLeft: 6 }}>Next</button>
      </div>

      {loading ? <p>Loading…</p> : (
        <table border="1" cellPadding="6" style={{ borderCollapse: "collapse", width: "100%" }}>
          <thead>
            <tr>
              <th>ID</th><th>Actor</th><th>Type</th><th>Outcome</th><th>IP</th><th>At</th><th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {events.map(ev => (
              <tr key={ev.event_id}>
                <td>{ev.event_id}</td>
                <td>{ev.actor_id} ({ev.actor_type})</td>
                <td>{ev.event_type}</td>
                <td>{ev.outcome}</td>
                <td>{ev.ip_address || "-"}</td>
                <td>{new Date(ev.occurred_at).toLocaleString()}</td>
                <td>
                  <button onClick={() => onEdit(ev.event_id)}>Edit</button>
                  <button onClick={() => onDelete(ev.event_id)} style={{ marginLeft: 6 }}>Delete</button>
                </td>
              </tr>
            ))}
            {events.length === 0 && (
              <tr><td colSpan={7} style={{ textAlign: "center" }}>No events</td></tr>
            )}
          </tbody>
        </table>
      )}

      {!!msg && <p style={{ marginTop: 10 }}>{msg}</p>}
    </div>
  );
}
