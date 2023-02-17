from faker import Faker

faker = Faker()


def faker_email(name: str, length: int = None, domain: str = "example.com"):
    """
    Generate fake email from name.

    Args:
        name: str. Name of user.
        length: Optional[int]. Fill this value to limit the length of email.
        domain: Optional[str]. Domain of email. By default, it is "example.com".

    Returns:
        email: str
    """
    email_domain = f"@{domain}"
    clean_name = name.lower().replace(" ", "_")
    if length:
        assert length > len(email_domain), (
            f"'length' parameter has to be greater than length of 'domain': "
            f"{length} < {email_domain} | {len(email_domain)}"
        )
        email_prefix = clean_name[: length - len(email_domain)]
    else:
        email_prefix = clean_name

    email = f"{email_prefix}{email_domain}"
    return email
