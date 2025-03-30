import { Button, Flex, Text, Title } from "@mantine/core";
import { useState, useEffect } from "react";

const SuccessInfo = ({ handleDownload }: { handleDownload: () => void }) => {
  const [animate, setAnimate] = useState(false);

  useEffect(() => {
    setAnimate(true);
  }, []);
  return (
    <>
      <Flex
        h={"100%"}
        direction={"column"}
        align={"center"}
        justify={"space-between"}
      >
        <Flex
          justify={"space-evenly"}
          direction={"column"}
          align={"center"}
          h={"80%"}
        >
          {/* <iframe src="https://lottie.host/embed/95b1ff77-e709-40d8-bcd2-80bdfb1d1dd3/p6hp7P0OqN.lottie"></iframe> */}
          <div
            className={`relative flex items-center justify-center w-24 h-24 rounded-full bg-green-500 ${
              animate ? "animate-ripple" : ""
            }`}
          >
            <div
              className={`w-10 h-6 border-l-6 border-b-6 border-white transform -rotate-45 opacity-0 transition-all duration-500 ease-out ${
                animate
                  ? "opacity-100 scale-100 translate-x-0 translate-y-0"
                  : "scale-50 translate-x-2 translate-y-2"
              }`}
            ></div>
          </div>

          <Title order={3}>AI did its thing :)</Title>
          <Text c="dimmed" ta={"center"}>
            Your file has been generated successfully.
          </Text>
        </Flex>

        <Button
          variant="filled"
          color="dark"
          size="md"
          radius="xl"
          onClick={handleDownload}
          w={"100%"}
        >
          Download
        </Button>
      </Flex>
    </>
  );
};

export default SuccessInfo;
