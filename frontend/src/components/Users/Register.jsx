import { useState } from "react";
import { registerUser } from "../../api/users";

export default function Register() {
  const [email, setEmail] = useState(""); const [password, setPassword] = useState("");
  const [msg, setMsg] = useState("");

  const submit = async () => {
    try {
      const res = await registerUser(email, password);
      setMsg(`User created: ${res.data.email}`);
    } catch (e) {
      setMsg(e.response?.data?.detail || "Register failed");
    }
  };

  return (
    <div>
      <h3>Register</h3>
      <input placeholder="email" value={email} onChange={(e)=>setEmail(e.target.value)} />
      <input placeholder="password" type="password" value={password} onChange={(e)=>setPassword(e.target.value)} />
      <button onClick={submit}>Register</button>
      {!!msg && <p>{msg}</p>}
    </div>
  );
}
