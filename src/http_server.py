"""Remote HTTP entry point for Instagram MCP."""

from contextlib import asynccontextmanager

from starlette.applications import Starlette
from starlette.routing import Mount

from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
from mcp.server.transport_security import TransportSecuritySettings

from . import instagram_mcp_server as instagram_module
from .instagram_client import InstagramClient
from .instagram_mcp_server import InstagramMCPServer


# Create the existing Instagram MCP server and its tools.
mcp_server = InstagramMCPServer()

# Configure the HTTP session manager for Render.
security = TransportSecuritySettings(
    allowed_hosts=[
        "instagram-mcp-8w5o.onrender.com",
        "instagram-mcp-8w5o.onrender.com:*",
    ],
)

session_manager = StreamableHTTPSessionManager(
    app=mcp_server.server,
    security_settings=security,
)


@asynccontextmanager
async def lifespan(app):
    """Initialize Instagram and manage HTTP sessions."""

    instagram_module.instagram_client = InstagramClient()

    is_valid = await instagram_module.instagram_client.validate_access_token()

    if not is_valid:
        raise RuntimeError("Instagram access token is invalid")

    print("Instagram access token validated successfully")

    async with session_manager.run():
        yield


# The MCP endpoint is /mcp.
app = Starlette(
    routes=[
        Mount("/mcp", app=session_manager.handle_request),
    ],
    lifespan=lifespan,
)
