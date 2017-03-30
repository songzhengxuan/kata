import json, requests
import time
import web

urls = (
    '/start', 'start',
    '/stop', 'stop'
)

class Client:
    m_interrupted = False

    def start_working(self):
        print "start working"
        m_interrupted = False
        while self.work("http://127.0.0.1:8080/GetJob") > 0:
            if m_interrupted:
                print "work interrupted"
                break;
            continue
        print "no more job todo, quit"
        return        
    
    def stop_working(self):
        print "stop working"
        m_interrupted = True

    def work(self, job_server_url):
        print "job server url is ", job_server_url
        resp = requests.get(url=job_server_url)
        print "get job desc", resp.text
        data = json.loads(resp.text)
        if data["rc"] <= 0:
            return data["rc"]
        return self.doJob(data["input"], data["output"])
    
    def doJob(self, input_ftp_file, output_ftp_folder):
        print "doJob called with input_ftp_file", input_ftp_file
        print "     output_ftp_folder", output_ftp_folder 
        time.sleep(10)
    
g_client = Client()

class start:
    def GET(self):
        print "start called"
        g_client.start_working()
        return "working started"

class stop:
    def GET(self):
        print "stop called"
        g_client.stop_working()
        return "working stopped"


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()