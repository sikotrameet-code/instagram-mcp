#!/usr/bin/env python3
"""
Instagram MCP Server - A Model Context Protocol server for Instagram API integration.

This server provides tools, resources, and prompts for interacting with Instagram's Graph API,
enabling AI applications to manage Instagram business accounts programmatically.
"""

import asyncio
import json
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional, Sequence

import structlog
from mcp.server import Server
from mcp.server.lowlevel.server import NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import Prompt, Resource, TextContent, Tool

from .config import get_settings
from .instagram_client import InstagramAPIError, InstagramClient
from .models.instagram_models import (
    InsightMetric,
    InsightPeriod,
    MCPToolResult,
    PublishMediaRequest,
    ReplyCommentRequest,
    SendDMRequest,
)

# Configure logging
logger = structlog.get_logger(__name__)

# Global Instagram client
instagram_client: Optional[InstagramClient] = None
