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
  const app = await addApp(parsed.value);
  revalidatePath("/admin/apps");
  return { ok: `Saved ${app.name} (${app.subdomain}.calecutech.com)` };
}
