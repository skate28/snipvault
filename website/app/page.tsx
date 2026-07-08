import { Nav } from "./components/Nav";
import { Hero } from "./components/Hero";
import { Install } from "./components/Install";
import { Features } from "./components/Features";
import { Usage } from "./components/Usage";
import { Footer } from "./components/Footer";

export default function Home() {
  return (
    <>
      <Nav />
      <main className="flex-1">
        <Hero />
        <Features />
        <Usage />
        <Install />
      </main>
      <Footer />
    </>
  );
}
