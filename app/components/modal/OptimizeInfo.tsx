import { Title, Card, List, Text } from "@mantine/core";

const OptimizeInfo = () => {
  return (
    <>
      <Title order={2} mt={10}>
        How to Optimize Your CV
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
            <strong>Step 1:</strong> Upload your existing CV in PDF format.
          </Text>
        </List.Item>

        <List.Item>
          <Text size="md">
            <strong>Step 2:</strong> Hit the "Submit" button to process your CV.
          </Text>
        </List.Item>

        <List.Item>
          <Text size="md">
            <strong>Step 3:</strong> Once processed, you will be able to
            download your CV by clicking the "Download" button.
          </Text>
        </List.Item>
      </List>
    </>
  );
};

export default OptimizeInfo;
