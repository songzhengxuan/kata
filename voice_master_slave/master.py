import web

urls = (
    '/GetJob', 'GetJob'
)

class Job_Queue:
    def init_job_queue(self):
        print "init job queue"
    
    def get_next_job(self):
        print "this is next_job"
        return "this is next job"


g_job_queue = Job_Queue()
g_job_queue.init_job_queue()

def get_job_fun():
    return "this is a job"

class GetJob:
    def GET(self):
        return g_job_queue.get_next_job()

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()