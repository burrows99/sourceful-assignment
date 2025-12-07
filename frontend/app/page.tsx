import { PromptBox } from "@/components/ui";

export default function Home() {
  return (
    <main className="min-h-screen flex items-center justify-center px-5 lg:px-8 py-10">
      <div className="w-full max-w-3xl">
        <PromptBox />
      </div>
    </main>
  );
}
