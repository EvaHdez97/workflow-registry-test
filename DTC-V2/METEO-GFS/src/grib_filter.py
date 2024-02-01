from datetime import timedelta
import requests
from dtcv2_util import log_management as logf 
import os

class GribFilter:
    

    def __init__(self, args):
        #time arguments
        self.date     = args.date
        self.cycle    = args.cycle
        self.step     = args.step
        self.it1      = args.time[0]
        self.it2      = args.time[1]+1
        self.time_ref = args.date + timedelta(hours=args.cycle)

        #lat arguments
        self.latmin = args.latmin
        self.latmax = args.latmax

        #lon arguments
        self.lonmin = args.lonmin
        self.lonmax = args.lonmax

        #spatial resolution
        self.res    = args.res


        #output file
        self.output = args.output
        self.path= args.path
        #verbose option
        self.verbose = args.verbose
        
        #Status of download
        self.status=0
        
        #Read the server config (all server.json configurations)
        self.server= args.server 
        self.var_list = args.var_list
        self.lev_list = args.lev_list
        
        #self Messages for log.json
        self.identifier="GFS_download"
        self.log_file=args.log_file
    def save_data(self):
        
        if self.verbose: logf.write_log(self.log_file, "Saving GFS data in folder ...", "INFORMATION", self.identifier,"100") 
        for it in range(self.it1,self.it2,self.step):
            #forecast hour
            fh  = it
            URL = self._getURL(fh)
            if self.verbose: logf.write_log(self.log_file, "Working for forecast time "+str(fh), "INFORMATION", self.identifier,"100") 
            #if self.verbose:logf.write_log(self.log_file,"Opening "+str(URL), "INFORMATION", self.identifier)
            local_filename = str(os.path.join(self.path,"{fh:03d}-{basename}".format(basename = self.output,
                                                      fh       = it)
                                                      ))
            
            self._downloadFile(URL,local_filename)
            
            if self.status ==404:
                logf.write_log(self.log_file,"The element does not exists. Please check the information given", "ERROR", self.identifier,"404")
                break
            if self.status==200:
                logf.write_log(self.log_file, "Downloaded forecast time "+str(fh), "SUCCESS", self.identifier,"200")  
    def _getURL(self,fh):
        if self.res==0.25:
            res = "0p25"
            ext = "pgrb2"
        elif self.res==0.5:
            res = "0p50"
            ext = "pgrb2full"
        elif self.res==1.0:
            res = "1p00"
            ext = "pgrb2"
        URL = "https://{server}/cgi-bin/filter_gfs_{res}.pl".format(server=self.server,res=res)
        #Append filename
        URL = URL + "?file=gfs.t{cycle:02d}z.{ext}.{res}.f{fhhh:03d}".format(cycle = self.cycle,
                                                                             ext   = ext,
                                                                             res   = res, 
                                                                             fhhh  = fh )
        #Append level list
        #URL = URL + "".join(["&lev_"+item+"=on" for item in self.lev_list])
        URL = URL + "&all_lev=on"
        #Append variable list
        URL = URL + "".join(["&var_"+item+"=on" for item in self.var_list])
        #Append subste information
        URL = URL + "&subregion=&leftlon={lonmin}&rightlon={lonmax}&toplat={latmax}&bottomlat={latmin}".format(lonmin = self.lonmin,
                                                                                                               lonmax = self.lonmax,
                                                                                                               latmin = self.latmin,
                                                                                                               latmax = self.latmax )
        #Append
        URL = URL + "&dir=%2Fgfs.{date}%2F{cycle:02d}%2Fatmos".format(date  = self.time_ref.strftime("%Y%m%d"),
                                                                     cycle = self.cycle)
        
        return URL

    def _downloadFile(self,url,local_filename):
        try:
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with open(local_filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192): 
                        if chunk: # filter out keep-alive new chunks
                            f.write(chunk)
                            # f.flush()
            self.status=r.status_code   
        except Exception as e:
            logf.write_log(self.log_file,str(e), "ERROR", self.identifier,"404") 
            self.status=r.status_code
    
    
        

class GFS(GribFilter):
                 

    def __init__(self, args):
        super().__init__(args)
        
    

        