"use server";

import { revalidatePath } from "next/cache";
import { isAdmin } from "@/lib/admin-auth";
import { addApp } from "@/lib/apps-store";
import { parseNewApp } from "@/lib/validate";

export type FormState = { error?: string; ok?: string };

export async function createApp(_prev: FormState, form: FormData): Promise<FormState> {
  if (!(await isAdmin())) return { error: "Not signed in." };
  const parsed = parseNewApp(form);
  if (!parsed.ok) return { error: parsed.error };
  let app;
  try {
    app = await addApp(parsed.value);
  } catch (e) {
    return { error: e instanceof Error ? e.message : "Could not save." };
  }
  revalidatePath("/admin/apps");
  return { ok: `Saved ${app.name} (${app.subdomain}.calecutech.com)` };
}
