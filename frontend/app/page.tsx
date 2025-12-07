import { PromptBox } from "@/components/ui";

export default function Home() {
  return (
    <main className="grid grid-cols-12 gap-5 px-5 lg:px-8 py-10">
      <div className="col-span-full lg:col-span-8 lg:col-start-3">
        <PromptBox />
      </div>
    </main>
  );
}
