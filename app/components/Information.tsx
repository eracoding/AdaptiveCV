import { ActionIcon, Affix, Modal } from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";
import GenerateInfo from "./modal/GenerateInfo";
import OptimizeInfo from "./modal/OptimizeInfo";

const Information = ({ type }: { type: string }) => {
  const [opened, { open, close }] = useDisclosure(false);

  return (
    <>
      <Modal
        size={"lg"}
        opened={opened}
        onClose={close}
        withCloseButton={false}
      >
        {type === "generate" ? <GenerateInfo /> : <OptimizeInfo />}
      </Modal>

      <Affix position={{ bottom: 20, right: 20 }}>
        <ActionIcon
          variant="default"
          size={52}
          radius="xl"
          aria-label="Information"
          color="black"
          onClick={open}
        >
          ?
        </ActionIcon>
      </Affix>
    </>
  );
};

export default Information;
