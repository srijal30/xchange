def valid_email( email : str ) -> bool :
    """
    checks whether email is a valid email
    """
    if "@" not in email:
        return False
    if email.count("@") > 1:
        return False
    left, right = email.split("@")
    if len(left) < 1 or len(right) < 1:
        return False
    return True

