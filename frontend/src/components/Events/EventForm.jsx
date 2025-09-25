import { useState, useEffect } from "react";
import { createEvent, replaceEvent, patchEvent } from "../../api/events";

const DEFAULTS = {
  actor_id: 1,
  actor_type: "admin",
  event_type: "login",
  outcome: "success",
  ip_address: "127.0.0.1",
  user_agent: "ViteFrontend/1.0",
  auth_method: "password",
  provider: "local",
  mfa_used: false,
  failure_reason: null,
  log_level: "INFO",
};

export default function EventForm({ initial, onDone }) {
  const isEditing = !!initial;
  const [form, setForm] = useState(DEFAULTS);
  const [usePatch, setUsePatch] = useState(false);
  const [msg, setMsg] = useState("");

  useEffect(() => {
    if (initial) {
      // fill with existing event
      const { event_id, occurred_at, ...rest } = initial;
      setForm({ ...DEFAULTS, ...rest, failure_reason: rest.failure_reason ?? null });
    }
  }, [initial]);

  const update = (k, v) => setForm(prev => ({ ...prev, [k]: v }));

  const submit = async () => {
    try {
      // if outcome is failure and reason empty -> API validation will reject; we set a default here to help UX
      if (form.outcome === "failure" && !form.failure_reason) {
        setMsg("failure_reason is required when outcome = failure");
        return;
      }
      if (!isEditing) {
        await createEvent(form);
        setMsg("Created");
      } else {
        if (usePatch) {
          const changes = {}; // partial
          Object.keys(form).forEach(k => {
            if (form[k] !== initial[k]) changes[k] = form[k];
          });
          await patchEvent(initial.event_id, changes);
          setMsg("Updated (PATCH)");
        } else {
          await replaceEvent(initial.event_id, form);
          setMsg("Updated (PUT)");
        }
      }
      onDone?.();
      setForm(DEFAULTS);
    } catch (e) {
      setMsg(e.response?.data?.detail || "Save failed");
    }
  };

  return (
    <div style={{ border: "1px solid #ddd", padding: 12, borderRadius: 8, marginBottom: 12 }}>
      <h3>{isEditing ? "Edit Event" : "Create Event"}</h3>

      <div style={{ display: "grid", gap: 8, gridTemplateColumns: "repeat(2, minmax(220px, 1fr))" }}>
        <label>Actor ID <input type="number" value={form.actor_id} onChange={e => update("actor_id", +e.target.value)} /></label>
        <label>Actor Type
          <select value={form.actor_type} onChange={e => update("actor_type", e.target.value)}>
            <option>user</option><option>admin</option><option>service</option>
          </select>
        </label>

        <label>Event Type <input value={form.event_type} onChange={e => update("event_type", e.target.value)} /></label>
        <label>Outcome
          <select value={form.outcome} onChange={e => update("outcome", e.target.value)}>
            <option>success</option><option>failure</option>
          </select>
        </label>

        <label>IP Address <input value={form.ip_address || ""} onChange={e => update("ip_address", e.target.value || null)} /></label>
        <label>User Agent <input value={form.user_agent || ""} onChange={e => update("user_agent", e.target.value || null)} /></label>

        <label>Auth Method <input value={form.auth_method || ""} onChange={e => update("auth_method", e.target.value || null)} /></label>
        <label>Provider <input value={form.provider || ""} onChange={e => update("provider", e.target.value || null)} /></label>

        <label>MFA Used
          <select value={form.mfa_used ? "true" : "false"} onChange={e => update("mfa_used", e.target.value === "true")}>
            <option value="false">false</option>
            <option value="true">true</option>
          </select>
        </label>

        <label>Failure Reason <input value={form.failure_reason || ""} onChange={e => update("failure_reason", e.target.value || null)} /></label>
        <label>Log Level
          <select value={form.log_level} onChange={e => update("log_level", e.target.value)}>
            <option>INFO</option><option>WARN</option><option>ERROR</option>
          </select>
        </label>
      </div>

      {isEditing && (
        <label style={{ display: "block", margin: "8px 0" }}>
          <input type="checkbox" checked={usePatch} onChange={(e) => setUsePatch(e.target.checked)} />
          {" "}Use PATCH (partial) instead of PUT (full)
        </label>
      )}

      <button onClick={submit} style={{ marginTop: 8 }}>{isEditing ? "Save" : "Create"}</button>
      {!!msg && <p style={{ marginTop: 6 }}>{msg}</p>}
    </div>
  );
}
