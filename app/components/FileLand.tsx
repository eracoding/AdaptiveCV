import { Title, Text, Card, Flex } from "@mantine/core";
import Info from "./icon/Info";

const FileLand = () => {
  return (
    <>
      <Card withBorder bg={"none"} shadow="xs" h={"100%"}>
        <Flex h={'100%'} direction={"column"} align={"center"} justify={'space-evenly'}>
          <Info color="#868E96" width={150} height={150} />

          <div> 
            <Title ta={"center"} c="dimmed">
              Your brand new CV
            </Title>
            <Text ta={"center"} c="dimmed">
              This is where your new CV will appear
            </Text>
          </div>
        </Flex>
      </Card>
    </>
  );
};

export default FileLand;
