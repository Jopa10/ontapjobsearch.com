import type { Metadata } from "next";
import Link from "next/link";

const canonicalUrl = "https://www.ontapjobsearch.com/ai-course-reviews";

export const metadata: Metadata = {
  title: "AI Course Reviews for Beginners and Office Workers | Ontap",
  description:
    "First-hand reviews of beginner AI courses, including Elements of AI and OpenAI Academy's AI Foundations, for people who want practical skills for work.",
  alternates: { canonical: canonicalUrl },
};

const elementsChapters = [
  ["What is AI?", "Definitions, related fields and philosophical questions, including the Chinese Room thought experiment."],
  ["AI problem solving", "Search, problem-solving methods and games."],
  ["Real-world AI", "Probability, Bayes' rule and a spam-filter example using Naive Bayes."],
  ["Machine learning", "Types of learning, nearest-neighbour classification and regression."],
  ["Neural networks", "The basics, how networks are built and more advanced techniques."],
  ["Implications", "Predictions about the future and AI's effects on society."],
];

export default function AiCourseReviewsPage() {
  return (
    <main className="mx-auto max-w-4xl px-5 py-10 sm:px-6 sm:py-14">
      <nav aria-label="Breadcrumb" className="mb-6 text-sm text-slate-600">
        <ol className="flex flex-wrap items-center gap-2">
          <li><Link href="/" className="underline-offset-4 hover:underline">Home</Link></li>
          <li aria-hidden="true">&gt;</li>
          <li aria-current="page" className="font-medium text-slate-900">AI course reviews</li>
        </ol>
      </nav>

      <header className="mb-10">
        <p className="mb-3 text-sm font-bold uppercase tracking-wider text-blue-700">Ontap course reviews</p>
        <h1 className="mb-4 text-3xl font-extrabold tracking-tight text-slate-950 sm:text-4xl">
          Beginner AI course reviews: what is useful for work?
        </h1>
        <p className="max-w-3xl text-lg leading-8 text-slate-700">
          These are first-hand impressions of AI courses for people who want to understand the basics and use AI in everyday work. I look at what each course teaches, how practical it feels and who is most likely to find it useful.
        </p>
        <p className="mt-3 text-sm text-slate-500">Reviewed October 2026. Course content and access terms can change.</p>
      </header>

      <article className="mb-10 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8">
        <h2 className="mb-2 text-2xl font-bold text-slate-950">
          Elements of AI: a thoughtful introduction, but a theoretical one
        </h2>
        <p className="mb-6 text-slate-600">
          <a href="https://course.elementsofai.com/" className="font-semibold text-blue-700 underline underline-offset-4 hover:text-blue-900">
            Open Elements of AI: Introduction to AI
          </a>
          <span> · Free online course · Six chapters</span>
        </p>

        <p className="mb-5 leading-7 text-slate-700">
          <em>Elements of AI: Introduction to AI</em> is a free course from the University of Helsinki and MinnaLearn. It has six chapters:
        </p>
        <ol className="mb-6 list-decimal space-y-2 pl-6 leading-7 text-slate-700">
          {elementsChapters.map(([title, description]) => (
            <li key={title}><strong>{title}:</strong> {description}</li>
          ))}
        </ol>

        <p className="mb-5 leading-7 text-slate-700">
          I found it informative, but more like an introductory university course than practical training for someone who wants to use AI in an office job. It explains the ideas behind AI through concepts, exercises and puzzles. Chapter 3, for example, works through probability and spam filtering.
        </p>
        <p className="mb-5 leading-7 text-slate-700">
          That gives you useful background, but there is less focus on practising everyday tasks with AI tools. If you want examples for emails, documents, research or other office work, you may find it takes a while to get to them.
        </p>
        <p className="leading-7 text-slate-700">
          There is a workplace angle: MinnaLearn also offers an LMS version for organisations. That means jobseekers may encounter <em>Elements of AI</em> if a future employer has bought it as staff training. It is a solid choice for understanding AI fundamentals, but I would not make it my first choice for learning how to use AI in day-to-day office work.
        </p>
      </article>

      <article className="mb-10 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8">
        <h2 className="mb-2 text-2xl font-bold text-slate-950">OpenAI Academy: AI Foundations</h2>
        <p className="mb-6 text-slate-600">
          <a href="https://academy.openai.com/public/courses/ai-foundations-dnq5w" className="font-semibold text-blue-700 underline underline-offset-4 hover:text-blue-900">
            Open AI Foundations
          </a>
          <span> · Free with a ChatGPT account · About 60–75 minutes</span>
        </p>

        <p className="mb-5 leading-7 text-slate-700">
          <em>AI Foundations</em> is the introductory course in OpenAI Academy&apos;s <em>Apply AI at Work</em> pathway. It covers AI and large language models, how ChatGPT works, writing clearer prompts, providing useful context, reviewing responses and using AI responsibly. The activities include workplace scenarios and knowledge checks—for example, deciding whether to ask ChatGPT to revise an answer, check its logic or verify information.
        </p>
        <p className="mb-5 leading-7 text-slate-700">
          This is a much more practical introduction for someone who wants to start using AI at work. It gives you enough background to understand the very basics of what you are using, then moves into examples and habits you can try. You can follow along with a free ChatGPT account, which is the whole hook of the training course.
        </p>
        <p className="mb-5 leading-7 text-slate-700">
          The presentation style may not suit everyone. I found the presenter and some of the polished, mission-led language irritating, and the course has a distinctly American corporate feel. It is good practice for the fist-gnawing irritation that dealing with ChatGPT can provoke over the long term—but there is no doubting that the practical material is useful. I liked the scenario-based checks once I had worked out how they operated. It is definitely not a course to do on autopilot; it involves a fair bit of thinking.
        </p>
        <p className="mb-5 leading-7 text-slate-700">
          This is the first course in a wider pathway. <em>Applied AI Foundations</em> moves on to building repeatable workflows; <em>Agents and Workflows</em> covers delegating structured tasks while setting boundaries and checking the results. If those terms do not mean much to you yet, start with <em>AI Foundations</em>: for a beginner who wants a practical starting point, it is the better fit.
        </p>
        <p className="leading-7 text-slate-700">
          <a href="https://academy.openai.com/pages/courses" className="font-semibold text-blue-700 underline underline-offset-4 hover:text-blue-900">
            See the full Apply AI at Work pathway
          </a>
        </p>
      </article>

      <aside className="rounded-2xl border border-blue-200 bg-blue-50 p-6">
        <h2 className="mb-2 text-xl font-bold text-slate-950">Want practical examples to try?</h2>
        <p className="mb-4 leading-7 text-slate-700">
          See Ontap&apos;s straightforward AI tips for everyday office tasks, including prompts you can adapt.
        </p>
        <Link href="/ai-tips" className="font-bold text-blue-800 underline underline-offset-4 hover:text-blue-950">
          Read the practical AI tips →
        </Link>
      </aside>
    </main>
  );
}
