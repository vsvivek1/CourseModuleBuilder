// Tickable features for a new module. Exam-specific pages are not offered.
export const FEATURES = [
  { id: "quizzes", label: "Timed quizzes, leaderboard, results" },
  { id: "question_banks", label: "Question banks and file import" },
  { id: "ai_questions", label: "AI question generator" },
  { id: "facts", label: "Fact generator" },
  { id: "schedule", label: "365-day content schedule" },
  { id: "social", label: "Publish to YouTube, Instagram, Facebook" },
  { id: "affiliates", label: "Affiliate product links" },
  { id: "emails", label: "Invite and result emails" },
  { id: "payments", label: "Paid courses and quiz series (Pro)" },
  { id: "android", label: "Android app (Play Store build)" },
] as const;

export type FeatureId = (typeof FEATURES)[number]["id"];

const IDS = new Set<string>(FEATURES.map((f) => f.id));

export function parseFeatures(values: FormDataEntryValue[]): FeatureId[] {
  return values.map(String).filter((v): v is FeatureId => IDS.has(v));
}
