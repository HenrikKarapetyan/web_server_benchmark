import threading
from time import sleep, time
from curl import request

successfull_requests_count = 0
un_successfull_requests_count = 0


class Requester(threading.Thread):
    def __init__(self, uri, name, requests_count, headers={}, user_agent="PostmanRuntime/7.15.2", verbose=False):
        super().__init__()
        self.name = name
        self.uri = uri
        self.user_agent = user_agent
        self.headers = headers
        self.requests_count = requests_count
        self.verbose = verbose

    def run(self):

        global successfull_requests_count
        global un_successfull_requests_count

        for _ in range(0, self.requests_count):

            sleep(1)
            resp = request(
                uri=self.uri,
                ssl_verify=False,
                verbose=self.verbose,
                headers=self.headers,
                user_agent=self.user_agent
            )
            if resp['res_code'] == 200:
                successfull_requests_count += 1
            else:
                un_successfull_requests_count += 1

            # print(self.name, 'request number ' + str(i), resp['res_code'])


class ThreadsLifeChecker(threading.Thread):

    def __init__(self, thread_objects):
        super().__init__()
        self.thread_objects = thread_objects

    def run(self):

        while True:
            alive_threads_count = 0
            for thread in self.thread_objects:
                if thread.is_alive():
                    alive_threads_count += 1
            if alive_threads_count == 0:
                end = time()
                print("sended requests count is: ", (threads_count * thread_requests_count))
                print("success requests count is: ", successfull_requests_count)
                print("unsuccess requests count is: ", un_successfull_requests_count)
                print("execution time is: ", (end - start))
                break
            sleep(0.2)


if __name__ == '__main__':
    threads_count = 100
    thread_requests_count = 4
    thread_objects_array = []
    start = time()
    for i in range(0, threads_count):
        th_object = Requester(uri="http://google.com", name="Thread " + str(i), requests_count=thread_requests_count)
        thread_objects_array.append(th_object)
        th_object.start()
        sleep(0.1)
    ThreadsLifeChecker(thread_objects=thread_objects_array).start()
