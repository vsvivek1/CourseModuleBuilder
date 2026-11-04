"use server";

import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import { ADMIN_COOKIE } from "@/lib/admin-auth";

export async function login(form: FormData) {
  const token = process.env.ADMIN_TOKEN;
  const given = String(form.get("token") ?? "");
  if (!token || given !== token) redirect("/admin/login?error=1");
  const jar = await cookies();
  jar.set(ADMIN_COOKIE, token, { httpOnly: true, secure: true, sameSite: "lax", path: "/admin" });
  redirect("/admin/apps");
}
