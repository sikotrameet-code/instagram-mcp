"""Remote HTTP entry point for Instagram MCP."""

from contextlib import asynccontextmanager

from starlette.applications import Starlette
from starlette.routing import Mount
from mcp.server.transport_security import TransportSecuritySettings

from . import instagram_mcp_server as instagram_module
from .instagram_client import InstagramClient
from .instagram_mcp_server import InstagramMCPServer


# Create the existing server and register all its tools.
mcp_server = InstagramMCPServer()
from importlib.metadata import version
print("INSTALLED MCP VERSION:", version("mcp"))

# Create the Streamable HTTP application.
security = TransportSecuritySettings(
    allowed_hosts=[
        "instagram-mcp-8w5o.onrender.com",
        "instagram-mcp-8w5o.onrender.com:*",
    ],
)

mcp_http_app = mcp_server.server.streamable_http_app(
    transport_security=security
)

@asynccontextmanager
async def lifespan(app):
    """Initialize Instagram and manage MCP sessions."""

    instagram_module.instagram_client = InstagramClient()

    is_valid = await instagram_module.instagram_client.validate_access_token()

    if not is_valid:
        raise RuntimeError("Instagram access token is invalid")

    print("Instagram access token validated successfully")

    async with mcp_server.server.session_manager.run():
        yield


# Expose the MCP endpoint at /mcp.
app = Starlette(
    routes=[
        Mount("/", app=mcp_http_app),
    ],
    lifespan=lifespan,
)
