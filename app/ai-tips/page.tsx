import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";

const canonicalUrl = "https://www.ontapjobsearch.com/ai-tips";

export const metadata: Metadata = {
  title: "Practical AI Tips for Admin Work | Ontap Job Search",
  description:
    "Simple, practical ways to use AI for admin, customer service and office-support work, with example prompts and sensible safety checks.",
  alternates: { canonical: canonicalUrl },
};

const tips = [
  {
    title: "Turn rough notes into actions",
    copy: "Ask AI to pull out decisions, actions, owners and deadlines from untidy meeting notes.",
    prompt:
      "Turn these notes into four headings: Decisions, Actions, Owner and Deadline. Flag anything unclear rather than guessing.",
  },
  {
    title: "Draft a clearer email",
    copy: "Give it the facts, the audience and the tone you want. Then check and personalise the draft.",
    prompt:
      "Draft a friendly, professional email using these facts. Keep it under 150 words and finish with a clear next step.",
  },
  {
    title: "Simplify a document",
    copy: "Use AI to make instructions or information easier to scan without losing important details.",
    prompt:
      "Rewrite this in plain English. Use short sentences and bullets where helpful. Keep every date, amount and required action unchanged.",
  },
  {
    title: "Improve a customer reply",
    copy: "Ask for a calm, helpful first draft that acknowledges the issue and explains what happens next.",
    prompt:
      "Improve this customer reply. Make it calm and helpful, avoid blame, and state clearly what we can do next. Do not invent a promise.",
  },
];

export default function AiTipsPage() {
  return (
    <main className="mx-auto max-w-5xl px-5 py-10 sm:px-6 sm:py-14">
      <section className="grid items-center gap-8 rounded-3xl border border-blue-100 bg-gradient-to-br from-blue-50 to-white p-6 sm:p-9 md:grid-cols-[1fr_240px]">
        <div>
          <p className="mb-3 text-sm font-bold uppercase tracking-wider text-blue-700">
            Ontap AI tips
          </p>
          <h1 className="mb-4 text-3xl font-extrabold tracking-tight text-slate-950 sm:text-4xl">
            Practical AI help for everyday work
          </h1>
          <p className="max-w-2xl text-lg leading-8 text-slate-700">
            AI&apos;s immediate value is practical: useful work, less theatre. Think of it
            as a very fast, enthusiastic—but inexperienced—assistant.
          </p>
        </div>
        <Image
          src="/assets/ontap-ai-robot-animated.webp"
          alt="Ontap's friendly AI helper waving"
          width={240}
          height={240}
          unoptimized
          priority
          className="mx-auto h-auto w-44 sm:w-52 md:w-60"
        />
      </section>

      <section className="py-10" aria-labelledby="everyday-tasks">
        <h2 id="everyday-tasks" className="mb-2 text-2xl font-bold text-slate-950">
          Four useful places to start
        </h2>
        <p className="mb-7 max-w-3xl leading-7 text-slate-600">
          Copy a prompt, replace the general wording with your own information, and
          treat the result as a first draft—not a finished answer.
        </p>
        <div className="grid gap-5 md:grid-cols-2">
          {tips.map((tip) => (
            <article key={tip.title} className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
              <h3 className="mb-2 text-lg font-bold text-slate-950">{tip.title}</h3>
              <p className="mb-4 leading-6 text-slate-600">{tip.copy}</p>
              <div className="rounded-xl bg-slate-50 p-4 text-sm leading-6 text-slate-800">
                <span className="font-bold text-blue-700">Try:</span> “{tip.prompt}”
              </div>
            </article>
          ))}
        </div>
      </section>

      <section className="grid gap-5 pb-10 md:grid-cols-2">
        <div className="rounded-2xl bg-slate-900 p-6 text-white">
          <h2 className="mb-3 text-xl font-bold">You stay in charge</h2>
          <p className="leading-7 text-slate-200">
            AI can do some of the digging, but you decide where to dig, how deep to
            go—and whether a hole needs digging at all. If it starts in the wrong
            place, stop it, correct its assumptions and point it in the right direction.
          </p>
        </div>
        <div className="rounded-2xl border border-amber-200 bg-amber-50 p-6">
          <h2 className="mb-3 text-xl font-bold text-slate-950">Keep information safe</h2>
          <p className="leading-7 text-slate-700">
            Never paste personal, sensitive or confidential information into a public
            AI tool. Follow your employer&apos;s policy, check facts, and read every draft
            before you use or send it.
          </p>
        </div>
      </section>

      <section className="rounded-2xl border border-blue-200 bg-blue-50 p-6 text-center">
        <h2 className="mb-2 text-xl font-bold text-slate-950">Looking for your next role?</h2>
        <p className="mb-5 text-slate-700">
          Browse current admin, customer-service and office-support vacancies—no signup required.
        </p>
        <Link
          href="/browse-jobs"
          className="inline-flex rounded-xl bg-blue-600 px-5 py-3 font-bold text-white hover:bg-blue-700 focus:outline-none focus:ring-4 focus:ring-blue-200"
        >
          Browse current jobs →
        </Link>
      </section>
    </main>
  );
}
