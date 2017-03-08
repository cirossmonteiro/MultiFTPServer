import mechanize as mec, re, time, cookielib as ck
from bs4 import BeautifulSoup as bs

class Router:
    
    # Cisco
    
    def __init__(self):
        
        self.intern_ip = "192.168.0.1"
        self.page = {'login':"Docsis_system.asp",
                     'status':"Status.asp",
                     'filter':'SingleForwarding.asp'}
        self.__login = {'user':'admin',
                      'passw':'admin'}
        self.__br = mec.Browser()
        self.__br.set_handle_robots(False)
        self.__external_ip = None
        self.__cj = ck.LWPCookieJar()
        self.__br.set_cookiejar(self.__cj)
        self.__br.set_handle_equiv(True)
        self.__br.set_handle_redirect(True)

    def login(self, us = None, ps = None):

        url = "http://%s/%s"%(self.intern_ip, self.page['login'])
        self.__br.open(url)
        self.__br.select_form(nr = 0)
        if [us, ps] != [None, None]:
            self.__login['user'] = us
            self.__login['passw'] = ps
        self.__br.form['username_login'] = self.__login['user']
        self.__br.form['password_login'] = self.__login['passw']
        self.__br.submit()
        
    def update_external_ip(self):

        url = "http://%s/%s"%(self.intern_ip, self.page['status'])
        output = self.__br.open(url).read()
        external_ip = bs(output, 'html.parser')
        external_ip = str(external_ip.b.string)
        self.__external_ip = external_ip

    def external_ip(self):

        if self.__external_ip == None:

            self.update_external_ip()
            return self.__external_ip

    def change_status_door(self, nfilter = 1, enable = 1):

        url = "http://%s/%s"%(self.intern_ip, self.page['filter'])
        self.__br.open(url)
        self.__br.select_form(nr = 0)
        
        if enable:
            self.__br.find_control('PortFilteringEnable%d'%nfilter).items[0].selected=True
        else:
            self.__br.find_control('PortFilteringEnable%d'%nfilter).items[0].selected=False
            
        self.__br.submit()

    def set_start_door(self, nfilter = 1, start = 0):
        
        url = "http://%s/%s"%(self.intern_ip, self.page['filter'])
        self.__br.open(url)
        self.__br.select_form(nr = 0)
        self.__br.form['IpFilterPortStart%d'%nfilter] = start
        self.__br.submit()

    def set_end_door(self, nfilter = 1, start = 0):
        
        url = "http://%s/%s"%(self.intern_ip, self.page['filter'])
        self.__br.open(url)
        self.__br.select_form(nr = 0)
        self.__br.form['IpFilterPortEnd%d'%nfilter] = start
        self.__br.submit()

    def set_protocol(self, nfilter = 1, protocol = "Both"):
        
        values = {"TCP" : 4,
                  "UDP" : 3,
                  "Both" : 254}
        url = "http://%s/%s"%(self.intern_ip, self.page['filter'])
        self.__br.open(url)
        self.__br.select_form(nr = 0)
        self.__br.form['PortFilteringProtocol%d'%nfilter] = [str(values[protocol]),]
        self.__br.submit()

cisco = Router()
cisco.login()
myextip = cisco.external_ip()
print myextip

