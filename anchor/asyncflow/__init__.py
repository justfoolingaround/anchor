import asyncio
import contextvars
import inspect


def to_asyncio(f):
    """
    Convert a blocking function to a proper asyncio coroutine.
    """

    async def __inner__(*args, **kwargs):

        loop = asyncio.get_running_loop()
        ctx = contextvars.copy_context()

        return await loop.run_in_executor(None, ctx.run, f, *args, **kwargs)

    return __inner__


class AsyncClassFactory(type):
    """
    Sets up your class' functions with their
    asynchronous counterparts.
    """

    def __new__(cls, qualified_name, bases, namespace):

        target_class = super().__new__(cls, qualified_name, bases, namespace)
        class_dir = dir(target_class)

        for attrib in class_dir:

            item = getattr(target_class, attrib, None)

            if (
                item is None
                or (not inspect.isfunction(item))
                or attrib.startswith(("_", "async_"))
                or f"async_{attrib}" in class_dir
                or asyncio.iscoroutinefunction(item)
            ):
                continue

            setattr(target_class, f"async_{attrib}", to_asyncio(item))

        return target_class
