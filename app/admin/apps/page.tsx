import { redirect } from "next/navigation";
import { isAdmin } from "@/lib/admin-auth";
import { listApps } from "@/lib/apps-store";
import { NewAppForm } from "./new-app-form";

export const dynamic = "force-dynamic";

export default async function AppsPage() {
  if (!(await isAdmin())) redirect("/admin/login");
  const apps = await listApps();
  return (
    <main>
      <h1>Generated apps</h1>
      {apps.length === 0 ? <p>No apps yet.</p> : (
        <ul>
          {apps.map((a) => (
            <li key={a.id}>
              <strong>{a.name}</strong> · {a.subdomain}.calecutech.com · {a.topic} · {a.paymentProvider} · {(a.features ?? []).length} features
            </li>
          ))}
        </ul>
      )}
      <NewAppForm />
    </main>
  );
}
