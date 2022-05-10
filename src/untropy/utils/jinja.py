from jinja2.ext import Extension


class MustacheExtension(Extension):
    """Jinja2 extension to Templatify a string."""

    def __init__(self, environment):
        """Initialize the extension with the given environment."""
        super(MustacheExtension, self).__init__(environment)

        def mustache(text, *args):
            return f"{{{{ {text.format(*args)} }}}}"

        def beard(text, *args):
            return f"{{% {text.format(*args)} %}}"

        def quote(text):
            return f"'{text}'"

        def dquote(text):
            return f'"{text}"'

        environment.filters["mustache"] = mustache
        environment.filters["beard"] = beard
        environment.filters["quote"] = quote
        environment.filters["dquote"] = dquote
