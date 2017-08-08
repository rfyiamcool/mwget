# -*- coding: utf-8 -*-

import os
import time
import Queue
import shutil
import multiprocessing

import util


class FileMwget():
    def __init__(self, url, save_path=None, status_func=None, done_func=None, process_num=10,
                debug=False):
        self.url = url
        self.debug = debug

        if save_path is None:
            save_path = url.split('/')[-1]

        if save_path[0] != '/':
            save_path = os.path.join(os.getcwd(), save_path)
        self.save_path = save_path

        self.hash = util.md5(url)
        self.temp_dir = os.path.join(os.getcwd(), 'tmp')
        self.data_path = os.path.join(self.temp_dir, self.hash)

        self.meta = {}
        self.task_queue = multiprocessing.Queue()
        self.process_num = 10

        if hasattr(status_func, '__call__'):
            status_func("status")

        if hasattr(done_func, '__call__'):
            done_func('done')

        self.start_time = time.time()

    def print_msg(self, *args):
        if self.debug:
            print " ".join([str(a) for a in args])

    def init(self):
        if not os.path.exists(self.temp_dir) and not os.path.isdir(self.temp_dir):
            os.mkdir(self.temp_dir)
        if not os.path.exists(self.data_path) and not os.path.isdir(self.data_path):
            os.mkdir(self.data_path)

        size = util.get_source_size(self.url, 3)
        if size and size > 0:
            self.meta['size'] = size
            self.meta['size_readable'] = util.readable_size(size)
            if size > 1024 * 128:
                self.meta['num'] = size / 1024 / 128
            else:
                self.meta['num'] = 1
            self.meta['chunk_size'] = size / self.meta['num']
        else:
            raise Exception("Can't get content-length of %s" % self.url)

    def worker(self):
        while True:
            try:
                index = self.task_queue.get(True, 3)
                ck_path = self.chunk_path(index)
                if not os.path.exists(ck_path):
                    (_start, _end) = self.chunk_range(index)
                    data = util.download_chunk(self.url, _start, _end, 5)
                    if data:
                        with open(ck_path, 'w') as f:
                            f.write(data)
                else:
                    self.print_msg(ck_path, "exist")
            except Queue.Empty:
                self.print_msg(os.getpid(), 'has nothing to do and exit')
                break
            self.print_msg(self.progress())

    def progress(self):
        chunks = [f for f in os.listdir(self.data_path) if '-' in f]
        return len(chunks) * 1.0 / self.meta['num']

    def is_finished(self):
        """
        detect is file finish download
        :return: Boolean
        """
        if not os.path.exists(self.data_path):
            return False

        for i in range(0, self.meta['num']):
            if not os.path.exists(self.chunk_path(i)):
                return False
        return True

    def combine(self):
        if self.is_finished():
            self.end_time = time.time()
            self.elapsed_time = self.end_time - self.start_time
            with open(self.save_path, 'w') as f:
                for i in range(0, self.meta['num']):
                    ck_path = self.chunk_path(i)
                    with open(ck_path, 'r') as ck_file:
                        f.write(ck_file.read())
                self.print_msg(
                    "all done! elapsed time: %.3f" % self.elapsed_time)
        else:
            raise Exception("not finish download")

    def clean(self):
        if os.path.exists(self.data_path) and os.path.isdir(self.data_path):
            shutil.rmtree(self.data_path)

        if not os.listdir(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def chunk_range(self, index):
        _start = index * self.meta['chunk_size']
        _end = _start + self.meta['chunk_size'] - 1
        if index is self.meta['num'] - 1:
            _end += self.meta['size'] % self.meta['num']
        return _start, _end

    def chunk_path(self, index):
        _start = index * self.meta['chunk_size']
        _end = _start + self.meta['chunk_size'] - 1
        if index is self.meta['num'] - 1:
            _end += self.meta['size'] % self.meta['num']
        return os.path.join(self.data_path, str(_start) + '-' + str(_end))

    def run(self):
        self.init()
        self.print_msg("meta info:", self.meta)
        for i in range(0, self.meta['num']):
            self.task_queue.put(i)

        if self.meta['num'] < self.process_num:
            self.process_num = self.meta['num']
        pool = multiprocessing.Pool(self.process_num, self.worker)

        pool.close()
        pool.join()
        self.combine()
        self.clean()
        print "done!"

    def get_report(self):
        return {
            'size': self.meta['size'],
            'size_readable': self.meta['size_readable'],
            'num': self.meta['num'],
            'start_time': self.start_time,
            'end_time': self.end_time,
            'elapsed_time': self.elapsed_time,
            'speed': '%s/s' % util.readable_size(self.meta['size'] /
                                                 self.elapsed_time)
        }
