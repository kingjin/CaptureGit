# -*- coding: utf-8 -*-
import urllib2;
from BeautifulSoup import BeautifulSoup
import io;
import sys,os;
from git import Repo;
import threadpool;

#Git基本URL
gitpro_base_url = 'http://git.oschina.net{path}.git'

#抓取内容
def Capture(keys,page=1):
    siteurl="http://git.oschina.net/search?utf8=%E2%9C%93&search="+keys+"&page="+str(page);
    reqResult=urllib2.Request(siteurl);
    print reqResult;
    response=urllib2.urlopen(reqResult);
    content=response.read().decode("utf-8");
    return content;

#分析内容，并返回UrlList
def AnalysisContent(content):
    print len(content);
    soup=BeautifulSoup(content);
    soup.prettify();
    list=soup.findAll('span','pro-name');
    urlList=[];
    for item in list:
        #print (item.prettify());
        son= item.findAll('a');
        #print len(son);
        for sonItem in son:
            print sonItem
            urlList.append(sonItem.get('href'))
            print sonItem.get('href');
            print "--------";
    print(len(urlList));
    return urlList;

#Clone代码，并处理异常
def CloneGitByUrl(gitUrl,gitSavePath):
    try:
        Repo.clone_from(gitUrl, gitSavePath);
        print ""+gitUrl+" - "+gitSavePath;
    except Exception as ex:
        print "Error"+str(ex);

print ("开始执行代码")
#抓取指定列表页
list =[1,2,3,4,5];
#创建线程池 5线程
pool=threadpool.ThreadPool(5);
for pageItem in list:
    print (str(pageItem)+" =======")
    content= Capture('git',pageItem);
    urlList= AnalysisContent(content)
    #获取当前路径
    osPath=os.getcwd();
    saveFile=open(osPath+"\\"+str(pageItem)+".txt","w")
    print saveFile;
    for url in urlList:
        gitUrl=gitpro_base_url.format(path=url)
        saveFile.write(gitUrl);
        saveFile.write("\r\n");
        gitSavePath=osPath+"\\"+str(url).replace('/','_').replace('-','_');
        a = [gitUrl, gitSavePath];
        parms = [(a, None)];
        requests= threadpool.makeRequests(CloneGitByUrl,parms)
        for req in requests:
            pool.putRequest(req)

    saveFile.close();

pool.wait();