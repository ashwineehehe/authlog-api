import { useState } from "react";
import { login } from "../../api/users";

export default function Login() {
  const [email, setEmail] = useState(""); const [password, setPassword] = useState("");
  const [msg, setMsg] = useState("");

  const submit = async () => {
    try {
      const res = await login(email, password);
      localStorage.setItem("access_token", res.data.access_token);
      setMsg("Logged in ✔");
    } catch (e) {
      setMsg(e.response?.data?.detail || "Login failed");
    }
  };

  return (
    <div>
      <h3>Login</h3>
      <input placeholder="email" value={email} onChange={(e)=>setEmail(e.target.value)} />
      <input placeholder="password" type="password" value={password} onChange={(e)=>setPassword(e.target.value)} />
      <button onClick={submit}>Login</button>
      {!!msg && <p>{msg}</p>}
    </div>
  );
}
