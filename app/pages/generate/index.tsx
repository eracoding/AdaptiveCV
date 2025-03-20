import Layout from "@/components/wrapper/Layout";
import {
  ActionIcon,
  Button,
  Card,
  Group,
  SegmentedControl,
  SimpleGrid,
  Text,
  Title,
} from "@mantine/core";
import { useState } from "react";
import BasicPhoto from "@/components/icon/BasicFile";
import { Dropzone, DropzoneProps, PDF_MIME_TYPE } from "@mantine/dropzone";

const index = (props: Partial<DropzoneProps>) => {
  const [mode, setMode] = useState("generate");
  const [file, setFile] = useState<File | null>(null);

  console.log("file", file?.name);

  return (
    <>
      <Layout>
        <SegmentedControl
          mt={50}
          value={mode}
          onChange={setMode}
          data={[
            { label: "Generate", value: "generate" },
            { label: "Optimize", value: "optimize" },
          ]}
        />

        <SimpleGrid
          mt={50}
          cols={2}
          spacing={{ base: 10, sm: "xl" }}
          verticalSpacing={{ base: "md", sm: "xl" }}
        >
          <Card p={"sm"} shadow="sm" radius="md" withBorder w={"100%"}>
            <Title order={3} mb={12}>
              Upload file
            </Title>
            <Dropzone
              onDrop={(files) => {
                console.log("accepted files", files);
                setFile(files[0]);
              }}
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

            {/* preview file name */}
            {file && (
              <Card mt={12} className="!bg-[#e7e8e9]">
                <Group justify="space-between">
                  <Text truncate="end" w={"80%"}>
                    <span className="font-semibold">File Uploaded: </span>
                    {file.name}
                  </Text>

                  <ActionIcon
                    size={"md"}
                    variant="light"
                    aria-label="Remove file"
                    color="red"
                    onClick={() => setFile(null)}
                  >
                    X
                  </ActionIcon>
                </Group>
              </Card>
            )}

            <Button
              variant="filled"
              color="dark"
              size="md"
              radius="xl"
              mt={12}
              disabled={!file}
            >
              Submit
            </Button>
          </Card>

          <div className="border-red-100 border-2">2</div>
        </SimpleGrid>
      </Layout>
    </>
  );
};

export default index;

// bihan, i had a job in 2021 i was frontend dev...
