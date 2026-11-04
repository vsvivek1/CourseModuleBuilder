import "server-only";
import { promises as fs } from "node:fs";
import path from "node:path";
import type { FeatureId } from "./features";

// Step 1 storage: a JSON file. Replaced by a database in a later step.
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

export async function listApps(): Promise<AppSettings[]> {
  try {
    return JSON.parse(await fs.readFile(FILE, "utf8")) as AppSettings[];
  } catch {
    return [];
  }
}

export async function addApp(input: Omit<AppSettings, "id" | "createdAt">) {
  const apps = await listApps();
  const app: AppSettings = {
    ...input,
    id: crypto.randomUUID(),
    createdAt: new Date().toISOString(),
  };
  apps.push(app);
  await fs.mkdir(path.dirname(FILE), { recursive: true });
  await fs.writeFile(FILE, JSON.stringify(apps, null, 2));
  return app;
}
