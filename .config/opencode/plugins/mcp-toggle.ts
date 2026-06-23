import { type Plugin, tool } from "@opencode-ai/plugin";

export const McpTogglePlugin: Plugin = async ({ client }) => {
  return {
    tool: {
      mcp_toggle: tool({
        description: "Connect or disconnect an MCP server at runtime",
        args: {
          name: tool.schema.string().describe("MCP server name"),
          action: tool.schema.enum(["connect", "disconnect"]),
        },
        async execute(args) {
          if (args.action === "connect") {
            await client.mcp.connect({ name: args.name });
          } else {
            await client.mcp.disconnect({ name: args.name });
          }
          const status = await client.mcp.status();
          return `MCP "${args.name}" ${args.action}ed. Estado actual: ${JSON.stringify(status)}`;
        },
      }),
    },
  };
};
