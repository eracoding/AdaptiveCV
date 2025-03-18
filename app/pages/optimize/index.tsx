import BasicPhoto from "@/components/icon/BasicFile";
import Layout from "@/components/wrapper/Layout";

import { Button, Card, Flex, Group, Text } from "@mantine/core";
import { Dropzone, DropzoneProps, PDF_MIME_TYPE } from "@mantine/dropzone";

const index = (props: Partial<DropzoneProps>) => {
  return (
    <Layout>
      <Flex direction={"column"} justify={"center"} align={"center"} gap={"xl"}>
        <Card
          // className="mt-16 !bg-white/30 !shadow-md !ring-1 !ring-gray-900/5 !backdrop-blur-lg"
          className="mt-16"
          p={"sm"}
          shadow="sm"
          radius="md"
          withBorder
          w={"100%"}
        >
          <Dropzone
            onDrop={(files) => console.log("accepted files", files)}
            onReject={(files) => console.log("rejected files", files)}
            maxSize={5 * 1024 ** 2}
            accept={PDF_MIME_TYPE}
            {...props}
          >
            <Group
              justify="center"
              gap="xl"
              mih={220}
              style={{ pointerEvents: "none" }}
            >
              <Dropzone.Accept>
                <BasicPhoto />
              </Dropzone.Accept>
              <Dropzone.Reject>no</Dropzone.Reject>
              <Dropzone.Idle>
                <BasicPhoto />
              </Dropzone.Idle>

              <div>
                <Text size="xl" inline>
                  Drag files here or click to select files
                </Text>
                <Text size="sm" c="dimmed" inline mt={7}>
                  Attach only one file, the file should not exceed 5mb
                </Text>
              </div>
            </Group>
          </Dropzone>
        </Card>

        <Button variant="filled" color="dark" size="md" radius="xl">
          Submit
        </Button>
      </Flex>
    </Layout>
  );
};

export default index;
