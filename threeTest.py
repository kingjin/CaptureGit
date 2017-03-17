import threadpool
from git import Repo

#测试线程池用法

gitUrl="http://git.oschina.net/kingking/FlatUI";
def ShowLog(a,b):
    print(a+" ---"+b);
    Repo.clone_from(gitUrl,"C:\\CodeFile\\GitHub\\git-extras0\\")

pool=threadpool.ThreadPool(1);
a=["aa","bb"];
aa= [(a,None)];
request=threadpool.makeRequests(ShowLog,aa)
for req in request:
    pool.putRequest(req)
pool.wait();