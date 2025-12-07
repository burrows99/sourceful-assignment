import { PromptBox } from "@/components/ui";
import { AuthTestButtons } from "@/components/AuthTestButtons";

interface HomeProps {
  searchParams: Promise<{ category?: string }>;
}

export default async function Home({ searchParams }: HomeProps) {
  const params = await searchParams;
  
  return (
    <main className="min-h-screen flex items-center justify-center px-5 lg:px-16 py-10">
      <div className="w-full grid gap-4 md:gap-6 xl:gap-8 grid-cols-12 max-w-[1280px] mx-auto">
        {/* Auth Test Buttons */}
        <div className="col-span-full">
          <AuthTestButtons />
        </div>
        
        <div className="col-span-full lg:col-span-8 lg:col-start-3">
          <PromptBox initialCategory={params.category} />
        </div>
      </div>
    </main>
  );
}
