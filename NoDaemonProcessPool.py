import multiprocessing


# class NoDaemonProcess(multiprocessing.Process):
#     # make 'daemon' attribute always return False
#     def _get_daemon(self):
#         return False
# 
#     def _set_daemon(self, value):
#         pass
# 
#     daemon = property(_get_daemon, _set_daemon)
# 
# 
# # We sub-class multiprocessing.pool.Pool instead of multiprocessing.Pool
# # because the latter is only a wrapper function, not a proper class.
# class ProcessPool(multiprocessing.pool.Pool):
# 
#     Process = NoDaemonProcess


class NoDaemonProcess(multiprocessing.Process):
    @property
    def daemon(self):
        return False

    @daemon.setter
    def daemon(self, value):
        pass


class NoDaemonContext(type(multiprocessing.get_context())):
    Process = NoDaemonProcess

# We sub-class multiprocessing.pool.Pool instead of multiprocessing.Pool
# because the latter is only a wrapper function, not a proper class.
class ProcessPool(multiprocessing.pool.Pool):
    def __init__(self, *args, **kwargs):
        kwargs['context'] = NoDaemonContext()
        super(ProcessPool, self).__init__(*args, **kwargs)


# multi procs example
proc_bar = tqdm(total=txt_sum)
with multiprocessing.Pool(processes=multiprocessing.cpu_count()//2) as proc_pool:
    for root, dirs, files in os.walk(INPUT_DIR):
        for f in files:
            if '.txt' in f:
                tsv_path = os.path.join(root, f)
                proc_results.append(proc_pool.apply_async(tsv_proc, (tsv_path, tsv_path.replace(INPUT_DIR, OUTPUT_DIR)), callback=lambda _: proc_bar.update()))
    else:
        # wait until all thread is finished
        proc_pool.close()
        proc_pool.join()

# merge all result
sums = 0
for res in proc_results:
    c = res.get()
    sums += c
