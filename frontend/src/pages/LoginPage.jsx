import { useState } from "react";
import { useNavigate } from "react-router-dom";

import api from "../api/api";

function LoginPage() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function handleLogin(event) {
    event.preventDefault();
    setError("");

    try {
      const response = await api.post("/auth/login", {
        email,
        password,
      });

      localStorage.setItem("biosentinel_token", response.data.access_token);

      navigate("/map");
    } catch (error) {
      setError("E-mail ou senha inválidos.");
    }
  }

  return (
    <main className="login-page">
      <section className="login-card">
        <h1>BioSentinel</h1>
        <p>Monitoramento ambiental por dados de satélite</p>

        <form onSubmit={handleLogin}>
          <label>E-mail</label>
          <input
            type="email"
            value={email}
            placeholder={"Digite seu e-mail"}
            onChange={(event) => setEmail(event.target.value)}
          />

          <label>Senha</label>
          <input
            type="password"
            value={password}
            placeholder={"Digite sua senha"}
            onChange={(event) => setPassword(event.target.value)}
          />

          {error && <span className="error-message">{error}</span>}

          <button type="submit">Entrar</button>
        </form>
      </section>
    </main>
  );
}

export default LoginPage;