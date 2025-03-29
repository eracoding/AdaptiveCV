import '@mantine/core/styles.css';
import { createTheme, MantineProvider } from '@mantine/core'
import '@mantine/dropzone/styles.css';
import { Notifications } from '@mantine/notifications';
import '@mantine/notifications/styles.css';

import "@/styles/globals.css";
import type { AppProps } from "next/app";

const theme = createTheme({
  /** Put your mantine theme override here */
});

export default function App({ Component, pageProps }: AppProps) {
  return (
    <MantineProvider theme={theme}>
      <Notifications />
      <Component {...pageProps} />
    </MantineProvider>
  )
}
