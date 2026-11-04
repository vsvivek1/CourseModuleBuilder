import "server-only";
import { promises as fs } from "node:fs";
import path from "node:path";
import { get, put } from "@vercel/blob";
import type { FeatureId } from "./features";

// Storage: a private Vercel Blob (one JSON file) when BLOB_READ_WRITE_TOKEN is
// set, otherwise a local JSON file for development. A database replaces this later.
export type PaymentProvider = "razorpay" | "stripe";

export type AppSettings = {
  id: string;
  name: string;
  subdomain: string;
  topic: string;
  extraPrompt: string;
  paymentProvider: PaymentProvider;
  features: FeatureId[];
  createdAt: string;
};

const FILE = path.join(process.cwd(), "data", "apps.json");
const BLOB_PATH = "apps.json";
const useBlob = () => Boolean(process.env.BLOB_READ_WRITE_TOKEN);

async function readAll(): Promise<AppSettings[]> {
  try {
    if (useBlob()) {
      const res = await get(BLOB_PATH, { access: "private", useCache: false });
      if (!res || res.statusCode !== 200) return [];
      return JSON.parse(await new Response(res.stream).text()) as AppSettings[];
    }
    return JSON.parse(await fs.readFile(FILE, "utf8")) as AppSettings[];
  } catch {
    return [];
  }
}

async function writeAll(apps: AppSettings[]) {
  const body = JSON.stringify(apps, null, 2);
  if (useBlob()) {
    await put(BLOB_PATH, body, {
      access: "private",
      contentType: "application/json",
      addRandomSuffix: false,
      allowOverwrite: true,
    });
    return;
  }
  await fs.mkdir(path.dirname(FILE), { recursive: true });
  await fs.writeFile(FILE, body);
}

export async function listApps(): Promise<AppSettings[]> {
  return readAll();
}

export async function addApp(input: Omit<AppSettings, "id" | "createdAt">) {
  const apps = await readAll();
  if (apps.some((a) => a.subdomain === input.subdomain)) {
    throw new Error(`Subdomain "${input.subdomain}" is already used.`);
  }
  const app: AppSettings = {
    ...input,
    id: crypto.randomUUID(),
    createdAt: new Date().toISOString(),
  };
  apps.push(app);
  await writeAll(apps);
  return app;
}
