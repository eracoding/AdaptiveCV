import Layout from "@/components/wrapper/Layout";
import {
  ActionIcon,
  Button,
  Card,
  Group,
  Modal,
  SegmentedControl,
  SimpleGrid,
  Text,
  Textarea,
  Title,
} from "@mantine/core";
import { useState } from "react";
import BasicPhoto from "@/components/icon/BasicFile";
import { Dropzone, DropzoneProps, PDF_MIME_TYPE } from "@mantine/dropzone";
import classes from "@/styles/text.module.css";
import Information from "@/components/Information";
import { useDisclosure } from "@mantine/hooks";
import Loading from "@/components/modal/Loading";
import {
  handleDownload,
  handleFileUpload,
  handleTextUpload,
} from "@/utils/api";
import SuccessInfo from "@/components/SuccessInfo";
import FileLand from "@/components/FileLand";

const index = (props: Partial<DropzoneProps>) => {
  const [mode, setMode] = useState("generate");
  const [file, setFile] = useState<File | null>(null);
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);
  const [downloadUrl, setDownloadUrl] = useState<null | string>(null);
  const [opened, { open, close }] = useDisclosure(false); // for loading info model

  return (
    <>
      <Modal
        opened={opened}
        onClose={() => {}}
        centered
        withCloseButton={false}
        size={'xs'}
        overlayProps={{
          backgroundOpacity: 0.55,
          blur: 3,
        }}
      >
        <Loading />
      </Modal>

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
          cols={{ base: 1, sm: 1, md: 2, lg: 2 }}
          spacing={{ base: 10, sm: "xl" }}
          verticalSpacing={{ base: "md", sm: "xl" }}
        >
          {mode == "optimize" && (
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
                onClick={() =>
                  handleFileUpload(
                    file,
                    setLoading,
                    setDownloadUrl,
                    open,
                    close
                  )
                }
                loading={loading}
              >
                Submit
              </Button>
            </Card>
          )}

          {mode == "generate" && (
            <Card p={"sm"} shadow="sm" radius="md" withBorder w={"100%"}>
              <Title order={3} mb={12}>
                Enter Details
              </Title>

              <Textarea
                autoFocus
                placeholder="John Doe | MSc in Data Science | Python, Machine Learning | 3 years experience in AI research"
                mih={255}
                minRows={2}
                maxRows={4}
                value={prompt}
                onChange={(event) => setPrompt(event.currentTarget.value)}
                classNames={{
                  root: classes.root,
                  wrapper: classes.wrapper,
                  input: classes.input,
                }}
              />

              <Button
                variant="filled"
                color="dark"
                size="md"
                radius="xl"
                mt={12}
                disabled={!prompt}
                onClick={() =>
                  handleTextUpload(
                    setLoading,
                    setDownloadUrl,
                    open,
                    close
                  )
                }
                loading={loading}
              >
                Submit
              </Button>
            </Card>
          )}

          <Card
            p={"sm"}
            shadow="sm"
            radius="md"
            w={"100%"}
            className="border-2 border-dashed border-gray-300  !bg-white/30"
          >
            {/* big green success icon */}
            {/* download button */}
            {downloadUrl && <SuccessInfo />}

            {/* some big relevant icon/illustration */}
            {!downloadUrl && <FileLand />}

            {downloadUrl && (
              <button
                onClick={() => handleDownload(downloadUrl)}
                className="bg-gray-500 text-white p-2 w-full mt-2"
              >
                Download File
              </button>
            )}
          </Card>
        </SimpleGrid>
      </Layout>

      <Information type={mode} />
    </>
  );
};

export default index;
