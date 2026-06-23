import { execSync } from "child_process";
import type { Plugin } from "@opencode-ai/plugin";

const plugin: Plugin = async () => {
  return {
    event: async ({ event }) => {
      if (event.type !== "message.updated") return;
      const msg = event.properties.info;
      if (msg.role !== "assistant") return;
      if (!msg.time.completed) return;

      const elapsed = msg.time.completed - msg.time.created;
      if (elapsed >= 5000) {
        try {
          execSync(
            `notify-send -a opencode -i utilities-terminal "Query finished" "${Math.round(elapsed / 1000)}s"`,
            { timeout: 3000 },
          );
        } catch {
          // ignore
        }
      }
    },
  };
};

export default plugin;
