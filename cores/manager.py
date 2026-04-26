from concurrent.futures import ThreadPoolExecutor

class TaskManager:
    def __init__(self, root, max_workers=4):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.root = root

    def submit(self, func, on_success=None, on_error=None):
        future = self.executor.submit(func)

        def callback(future):

            try:
                result = future.result()
                if on_success:
                    try:
                        self.root.after(0, lambda: on_success(result))
                    except RuntimeError:
                        pass

            except Exception as e:
                if on_error:
                    try:
                        self.root.after(0, lambda: on_error(e))
                    except RuntimeError:
                        pass
                else:
                    print("Unhandled task error:", e)

        future.add_done_callback(callback)
        return future