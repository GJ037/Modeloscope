from concurrent.futures import ThreadPoolExecutor

class TaskManager:
    def __init__(self, root, max_workers=4):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.root = root

    def submit(self, func, success=None, failure=None):
        future = self.executor.submit(func)

        def callback(future):
            try:
                result = future.result()
                if success:
                    try:
                        self.root.after(0, lambda r=result: success(r))
                    except RuntimeError:
                        pass

            except Exception as error:
                if failure:
                    try:
                        self.root.after(0, lambda e=error: failure(e))
                    except RuntimeError:
                        pass
                else:
                    print("Unhandled task error:", error)

        future.add_done_callback(callback)
        return future