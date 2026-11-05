// RESOURCE_CALL 

permit(
    principal,
    action == Action::"call_resource",
    resource == Resource::"get_product"
)
when {
    principal.roles.contains("inventory-resource-role")
};

permit(
    principal,
    action == Action::"call_resource",
    resource == Resource::"get_inventory_service_info"
)
when {
    principal.roles.contains("inventory-resource-role")
};

// TOOL_CALLS

permit(
    principal,
    action == Action::"call_tool",
    resource == Tool::"patch_product"
)
when {
    principal.roles.contains("inventory-tool-role")
};

permit(
    principal,
    action == Action::"call_tool",
    resource == Tool::"post_product"
)
when {
    principal.roles.contains("inventory-tool-role")
};

permit(
    principal,
    action == Action::"call_tool",
    resource == Tool::"put_product"
)
when {
    principal.roles.contains("inventory-tool-role")
};