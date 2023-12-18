route_schemas = {
    '/marketplace/newModeration': {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "slack_url": {"type": "string", "format": "uri"},
            "dev_url": {"type": "string", "format": "uri"},
            "app_url": {"type": "string", "format": "uri"}
        },
        "required": ["name", "slack_url", "dev_url", "app_url"]
    }
}