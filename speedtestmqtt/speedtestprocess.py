import multiprocessing
import speedtest


class SpeedTest(multiprocessing.Process):

    def __init__(self):
        super(SpeedTest, self).__init__()
        self._finished = multiprocessing.Event()
        self._q = multiprocessing.Queue()
        
    def run(self):
        servers = []
        s = speedtest.Speedtest()
        s.get_servers(servers)
        s.get_best_server()
        s.download()
        s.upload()
        results = s.results.dict()
        self._q.put(results)
        self._finished.set()
        
    def finished(self):
        return self._finished.is_set()
        
    def get_results(self):
        if self._q.empty():
            return None
        else:
            return self._q.get()
