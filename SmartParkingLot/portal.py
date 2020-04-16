# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import cgi
from AnalysisLot import LotAnalyst
from LocateCar import CarLocator
import json

hostName = ""
serverPort = 8080
class MyServer(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        if self.path == "/lotAnalyst.html":
            path = os.path.dirname(os.path.abspath(__file__)) + '/lotAnalyst.html'
        elif self.path == "/carLocator.html":
            path = os.path.dirname(os.path.abspath(__file__)) + '/carLocator.html'
        else:
            path = os.path.dirname(os.path.abspath(__file__)) + '/index.html'
        fileHandler = open(path, 'r')
        self.wfile.write(bytes(fileHandler.read(), "utf-8"))
        fileHandler.close()

    def do_POST(self):
        rootPath = os.path.dirname(os.path.abspath(__file__))
        # Parse the form data posted
        form = cgi.FieldStorage(
            fp=self.rfile, 
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })
        respBody = ""
        if "imgFile" in form:
            imgFile = form["imgFile"]
            imgPath = rootPath + "/img/" + imgFile.filename
            if os.path.isfile(imgPath):
                os.remove(imgPath)
            fh = open(f"{imgPath}", "wb")
            fh.write(imgFile.value)
            fh.close()
            if '/parkingLots' == self.path:
                analyst = LotAnalyst(imgPath)
                lotReport = analyst.analysisLot()
                respBody = json.dumps(lotReport)
            elif '/carLocator' == self.path:
                carLocator = CarLocator(imgPath)
                respBody = json.dumps(carLocator.locateCar(form["platenum"].value))
        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytes(respBody, "utf-8"))


if __name__ == "__main__":    
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")