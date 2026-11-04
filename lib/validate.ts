export const SUBDOMAIN_RE = /^[a-z0-9](?:[a-z0-9-]{0,40}[a-z0-9])?$/;

export type NewAppInput = {
  name: string;
  subdomain: string;
  topic: string;
  extraPrompt: string;
  paymentProvider: "razorpay" | "stripe";
};

export function parseNewApp(form: FormData): { ok: true; value: NewAppInput } | { ok: false; error: string } {
  const get = (k: string) => String(form.get(k) ?? "").trim();
  const value: NewAppInput = {
    name: get("name"),
    subdomain: get("subdomain").toLowerCase(),
    topic: get("topic"),
    extraPrompt: get("extraPrompt"),
    paymentProvider: get("paymentProvider") === "stripe" ? "stripe" : "razorpay",
  };
  if (!value.name) return { ok: false, error: "Name is required." };
  if (!SUBDOMAIN_RE.test(value.subdomain)) {
    return { ok: false, error: "Subdomain: lowercase letters, digits and hyphens only." };
  }
  if (!value.topic) return { ok: false, error: "Topic is required." };
  return { ok: true, value };
}
