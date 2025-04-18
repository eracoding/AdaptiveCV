import { ActionIcon, Container, Flex, Group } from "@mantine/core";
import Image from "next/image";
import Link from "next/link";
import { useRouter } from "next/router";

const Layout = ({ children }: { children: React.ReactNode }) => {
  const router = useRouter();

  const NavButton = ({ link, name }: { link: string; name: string }) => {
    return (
      <Link
        href={link}
        className={`${
          router.pathname == link
            ? "bg-[#0A0A0A] text-white hover:bg-[#0A0A0A]"
            : "text-black hover:bg-[#ced0d3]"
        } px-5 py-2 rounded-full font-semibold transition`}
      >
        {name}
      </Link>
    );
  };

  return (
    <>
      <header className="h-16 bg-white/30 shadow-md ring-1 ring-gray-900/5 backdrop-blur-lg">
      {/* <header className="fixed top-0 left-0 w-full h-16 bg-white/30 shadow-md ring-1 ring-gray-900/5 backdrop-blur-lg z-50"> */}
        <Flex align={"center"} h={"100%"} px={"xl"} justify={"space-between"}>
          <ActionIcon
            variant="transparent"
            size={"xl"}
            onClick={() => router.push("/")}
            aria-label="logo"
          >
            <Image src="/logo.png" alt="logo" width={50} height={50} />
          </ActionIcon>
          {/* <Group gap="sm">
            <NavButton link={"/generate"} name={"Generate"} />
            <NavButton link={"/optimize"} name={"Optimize"} />
          </Group> */}
        </Flex>
      </header>

      <main>
        <Container size={"lg"} mt={"xl"} mb={"xl"}>
          {children}
        </Container>
      </main>
    </>
  );
};

export default Layout;
