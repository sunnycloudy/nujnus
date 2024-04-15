import functools
import click

class NujnusError(Exception):
    """自定义异常类"""

    def __init__(self, message="这是一个自定义的错误！"):
        self.message = message
        super().__init__(self.message)


def handle_exceptions(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NujnusError as e:
            click.echo(f"Error: {e.message}", err=True)
        except Exception as e:
            #click.echo(f"Unexpected Error: {e}", err=True)
            raise e

    return wrapper
