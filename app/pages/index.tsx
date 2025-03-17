import Image from "next/image";
import Link from 'next/link'
import ExpandingArrow from "@/components/expanding-arrow";
import { Suspense } from 'react'
import Welcome from "@/components/welcome";

export default function Home() {
  return (
    <main className="relative flex min-h-screen flex-col items-center justify-center">
      <Link
        href="https://vercel.com/templates/next.js/postgres-prisma"
        className="group mt-20 sm:mt-0 rounded-full flex space-x-1 bg-white/30 shadow-sm ring-1 ring-gray-900/5 text-gray-600 text-sm font-medium px-10 py-2 hover:shadow-lg active:shadow-sm transition-all"
      >
        <p>Let's Get Started</p>
        <ExpandingArrow />
      </Link>

      <h1 className="pt-4 pb-8 bg-gradient-to-br from-black via-[#171717] to-[#575757] bg-clip-text text-center text-4xl font-medium tracking-tight text-transparent md:text-7xl">
        AdaptiveCV
      </h1>

      {/* Centered message */}
      <Welcome />

      <p className="font-light text-gray-600 w-full max-w-lg text-center mt-6">
         An NLP project under {' '}
         <Link
          href="http://www.chaklam.com/"
          className="font-medium underline underline-offset-4 hover:text-black transition-colors"
         >
          Dr. Chaklam Silpasuwanchai
         </Link>
        <br /> Built with <span className="font-semibold">love</span> ❤️
      </p>

      <div className="flex justify-center space-x-5 pt-10 mt-10 border-t border-gray-300 w-full max-w-xl text-gray-600">
        <Link
          href="https://www.linkedin.com/in/ulugbek-shernazarov/"
          className="font-medium underline underline-offset-4 hover:text-black transition-colors"
        >
          Ulugbek
        </Link>
        <Link
          href="https://www.linkedin.com/in/bidhan-bajracharya-b87a5522a/"
          className="font-medium underline underline-offset-4 hover:text-black transition-colors"
        >
          Bidhan
        </Link>
        <Link
          href="https://www.linkedin.com/in/ishika~pradhan/"
          className="font-medium underline underline-offset-4 hover:text-black transition-colors"
        >
          Ishika
        </Link>
      </div>

      <div className="sm:absolute sm:bottom-0 w-full px-20 py-10 flex justify-between">
        <Link
          href="https://github.com/eracoding/AdaptiveCV"
          className="flex items-center space-x-2"
        >
          <Image
            src="/github.svg"
            alt="GitHub Logo"
            width={24}
            height={24}
            priority
          />
          <p className="font-light">Source</p>
        </Link>
      </div>
    </main>
  );
}
