const LoadingAnimation = () => {
  return (
    <div className="flex items-center justify-center">
      <video src="/dino-loading.webm" autoPlay loop muted className="w-40 h-40" />
      {/* <iframe src="https://lottie.host/embed/4f11808d-c62a-4df6-ac61-173c3eccac40/Xm8G8R5ORo.lottie"></iframe> */}
      {/* <iframe src="https://lottie.host/embed/41423c05-5650-4fcf-a327-58b59f978eda/CPVWP7MVFJ.lottie"></iframe> */}
    </div>
  );
};

export default LoadingAnimation;
