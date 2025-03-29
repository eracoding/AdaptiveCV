import { Title, Card, Text, List, Button, Group } from "@mantine/core";

const GenerateInfo = () => {
  return (
    <>
      <Title order={2} mt={10}>
        How to Generate Your CV
      </Title>

      {/* Placeholder for GIF */}
      <Card
        p="sm"
        radius="md"
        withBorder
        w="100%"
        h={200}
        mt={20}
        mb={20}
        style={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <Text c="dimmed">GIF Placeholder (Visualize the process)</Text>
      </Card>

      <Title order={3} mt={12}>
        Steps to Follow:
      </Title>

      <List spacing="sm" size="lg" style={{ marginTop: 20 }}>
        <List.Item>
          <Text size="md">
            <strong>Step 1:</strong> Enter the information you want to include
            in your CV.
          </Text>
        </List.Item>
        <List.Item>
          <Text size="md">
            <strong>Step 2:</strong> Review the dummy example shown below to
            understand the structure.
          </Text>
        </List.Item>
        <List.Item>
          <Text size="md">
            <strong>Step 3:</strong> Hit the "Submit" button to process your CV.
          </Text>
        </List.Item>
        <List.Item>
          <Text size="md">
            <strong>Step 4:</strong> Once processed, you will be able to
            download your CV by clicking the "Download" button.
          </Text>
        </List.Item>
      </List>

      <Card p={"sm"} radius="md" withBorder mt={20}>
        <Text fw={500} size="lg" ta="center" c="dimmed">
          Example personal information:
        </Text>

        <Text size="md" c="dimmed" mt={10}>
          <strong>Name:</strong> Jane Doe
          <br />
          <br />
          As a passionate software developer, I have over 5 years of experience
          in building scalable and efficient web applications. I've had the
          opportunity to work in both startup and corporate settings, where I
          specialized in front-end technologies like React and Vue, as well as
          back-end development with Node.js and Python. I'm also experienced in
          cloud computing and DevOps, which allows me to develop highly scalable
          systems and ensure smooth deployment processes.
          <br />
          <br />
          My technical skills are diverse and include proficiency in JavaScript,
          React, Node.js, Python, HTML, CSS, and SQL. I'm well-versed in using
          Git for version control and Agile methodologies for project
          management. I'm always looking to expand my skill set, and I'm
          currently diving into machine learning and serverless architecture. I
          thrive in collaborative environments and am dedicated to delivering
          top-notch solutions that make a real impact.
        </Text>
      </Card>
    </>
  );
};

export default GenerateInfo;
