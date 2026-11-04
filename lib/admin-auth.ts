import "server-only";
import { cookies } from "next/headers";

export const ADMIN_COOKIE = "cmb_admin";

export async function isAdmin(): Promise<boolean> {
  const token = process.env.ADMIN_TOKEN;
  if (!token) return false;
  const jar = await cookies();
  return jar.get(ADMIN_COOKIE)?.value === token;
}
