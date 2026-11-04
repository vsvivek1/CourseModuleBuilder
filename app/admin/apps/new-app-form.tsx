"use client";

import { useActionState } from "react";
import { FEATURES } from "@/lib/features";
import { createApp, type FormState } from "./actions";

const initial: FormState = {};

export function NewAppForm() {
  const [state, action, pending] = useActionState(createApp, initial);
  return (
    <form action={action}>
      <h2>New app</h2>
      <p><input name="name" placeholder="App name (e.g. JAIIB Prep)" required /></p>
      <p><input name="subdomain" placeholder="subdomain (e.g. jaiib)" required /> .calecutech.com</p>
      <p><input name="topic" placeholder="Topic (e.g. JAIIB exam)" required /></p>
      <p><textarea name="extraPrompt" rows={3} placeholder="Extra AI prompt for this app" /></p>
      <p>
        Payments:{" "}
        <select name="paymentProvider" defaultValue="razorpay">
          <option value="razorpay">Razorpay</option>
          <option value="stripe">Stripe</option>
        </select>
      </p>
      <fieldset>
        <legend>Features</legend>
        {FEATURES.map((f) => (
          <label key={f.id} style={{ display: "block" }}>
            <input type="checkbox" name="feature" value={f.id} defaultChecked /> {f.label}
          </label>
        ))}
      </fieldset>
      <button type="submit" disabled={pending}>Save app</button>
      {state.error && <p style={{ color: "crimson" }}>{state.error}</p>}
      {state.ok && <p style={{ color: "green" }}>{state.ok}</p>}
    </form>
  );
}
