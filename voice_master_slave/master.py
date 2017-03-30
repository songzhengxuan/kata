import web
from os import listdir
from os.path import join,isfile

urls = (
    '/GetJob', 'GetJob'
)

class Job_Queue:
    job_queue = []
    def init_job_queue(self, job_folder, result_folder):
        job_files = [f for f in listdir(job_folder) if isfile(join(job_folder, f))]
        result_files = [f for f in listdir(result_folder) if isfile(join(result_folder, f))]
        print job_files
        print result_files
        self.job_queue = []
        for jf in job_files:
            if jf in result_files:
                continue
            else:
                self.job_queue.append(jf)
        print "init job queue", self.job_queue

    def get_next_job(self):
        print "this is next_job"
        if len(self.job_queue) == 0:
            return '{"rc":0}'
        job_file = self.job_queue[0]
        return '{"rc":1, "input":"ftp://127.0.0.1/srv/ftp/job_folder/' + job_file + '", "output":"ftp://127.0.0.1/srv/ftp/result_folder"}'


g_job_queue = Job_Queue()
g_job_queue.init_job_queue("/srv/ftp/job_folder", "/srv/ftp/result_folder")

def get_job_fun():
    return "this is a job"

class GetJob:
    def GET(self):
        return g_job_queue.get_next_job()

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()