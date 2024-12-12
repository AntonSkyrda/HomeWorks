def create_form(*args):
    fields = "".join(
        [
            f'{arg.capitalize()}: <input type="text" name="{arg}" /> <br/>'
            for arg in args
        ]
    )

    return f"""
    <form method="post">
        {fields}
        <input type="submit" value="Submit" />
    </form>
    """
