from agents import function_tool

# @function_tool turns a Python function into a tool the LLM can call.
# The SDK builds the tool's JSON schema from the type hints and docstring.


@function_tool
def check_service_status() -> str:
    """Return the current mock service status."""
    print("  [tool] check_service_status()")
    return "All services are operational. Login, sync and web app are up."


@function_tool
def reset_password(email: str) -> str:
    """Send a password reset link to the given email address.

    Args:
        email: The customer's account email.
    """
    print(f"  [tool] reset_password({email!r})")
    return f"Password reset link sent to {email}. It expires in 30 minutes."


@function_tool
def create_technical_ticket(issue: str) -> str:
    """Open a technical support ticket for problems that can't be solved right away.

    Args:
        issue: Short description of the problem.
    """
    print(f"  [tool] create_technical_ticket({issue!r})")
    return "Technical ticket TECH-1042 created. The team will reply within 24 hours."


@function_tool
def get_subscription_info() -> str:
    """Return the customer's mock subscription details and recent payments."""
    print("  [tool] get_subscription_info()")
    return (
        "Plan: Pro (monthly), 199 TRY/month, status: active, next billing date: 2026-10-15. "
        "Recent payments: 2026-09-15 199 TRY, 2026-09-15 199 TRY, 2026-08-15 199 TRY. "
        "Invoices are available under Account > Billing > Invoices."
    )


@function_tool
def cancel_subscription() -> str:
    """Cancel the customer's subscription at the end of the billing period."""
    print("  [tool] cancel_subscription()")
    return "Subscription cancelled. The Pro plan stays active until 2026-10-15."


@function_tool
def create_billing_ticket(issue: str) -> str:
    """Open a billing ticket for refunds, duplicate charges or invoice problems.

    Args:
        issue: Short description of the billing problem.
    """
    print(f"  [tool] create_billing_ticket({issue!r})")
    return "Billing ticket BILL-2087 created. Refunds are processed within 5 business days."
