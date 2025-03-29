import { ActionIcon, Affix, Modal } from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";

const Information = () => {
  const [opened, { open, close }] = useDisclosure(false);

  return (
    <>
      <Modal opened={opened} onClose={close} withCloseButton={false}>
        Modal without header, press escape or click on overlay to close
        {/* A gif or video showing how to use it */}
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
