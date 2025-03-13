from typing import cast
from mcp.types import ListResourcesResult, Resource as MCPResource
from mcp.shared.exceptions import McpError
from langchain_mcp_adapters.client import MultiServerMCPClient


class MultiServerMCPClientWithResources(MultiServerMCPClient):

    async def list_resources(self, server_name: str) -> list[MCPResource]:
        if server_name not in self.sessions:
            raise ValueError(f"No active session for server '{server_name}'")

        try:
            response: ListResourcesResult = await self.sessions[
                server_name
            ].list_resources()
            return response.resources
        except McpError as e:
            raise RuntimeError(
                f"Failed to list resources on server '{server_name}': {str(e)}"
            )

    async def read_resource(
        self, server_name: str, uri: str
    ) -> tuple[bytes | str, str | None]:
        if server_name not in self.sessions:
            raise ValueError(f"No active session for server '{server_name}'")

        return await self.sessions[server_name].read_resource(uri)


import asyncio


async def main():
    config = {
        "myserver": {
            "transport": "sse",
            "url": "http://127.0.0.1:3000/sse",
        }
    }

    async with MultiServerMCPClientWithResources(config) as client:
        all_resources = await client.list_resources("myserver")
        print("Resources on myserver:", [r.uri for r in all_resources])

        content, mime_type = await client.read_resource("myserver", "resource://hello")
        print("Fetched content:", content)
        print("MIME type:", mime_type)


asyncio.run(main())
