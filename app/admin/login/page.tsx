import { login } from "./actions";

export default async function LoginPage({ searchParams }: { searchParams: Promise<{ error?: string }> }) {
  const { error } = await searchParams;
  return (
    <form action={login}>
      <h1>Admin sign-in</h1>
      {error && <p style={{ color: "crimson" }}>Wrong token.</p>}
      <input name="token" type="password" placeholder="Admin token" required />{" "}
      <button type="submit">Sign in</button>
    </form>
  );
}
