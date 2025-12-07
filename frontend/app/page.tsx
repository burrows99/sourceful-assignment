import { PromptBox } from "@/components/ui";

export default function Home() {
  return (
    <main className="min-h-screen flex items-center justify-center px-5 lg:px-16 py-10">
      <div className="w-full grid gap-4 md:gap-6 xl:gap-8 grid-cols-12 max-w-[1280px] mx-auto">
        <div className="col-span-full lg:col-span-8 lg:col-start-3">
          <PromptBox />
        </div>
      </div>
    </main>
  );
}
