const Welcome = () => {
  return (
    <div className="bg-white/30 p-12 shadow-xl ring-1 ring-gray-900/5 rounded-lg backdrop-blur-lg max-w-xl mx-auto w-full text-black">
        <h1 className="text-4xl font-semibold text-center">
            Welcome to the Vercel Postgres Demo
        </h1>
        <p className="text-gray-700 text-center mt-4">
            This is a demo of a Next.js app with a Postgres database deployed on Vercel.
        </p>
    </div>
  );
};

export default Welcome;
