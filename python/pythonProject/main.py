import pyodbc
import pymssql

sql_query = """
USE orion
/*
drop table #tmpPLog
drop table #tmpRes
*/
declare @startDate as datetime = '30.08.2021 00:00:00'
declare @endDate as datetime = '30.08.2021 23:59:59'

select * 
into #tmpPLog 
from pLogData WITH(index(idx_pLogData))
where IDComp in (0, 1, 2, 3, 5) and doorIndex in (4) and TimeVal between @startDate and DATEADD(day, 2, @endDate)
order by HozOrgan, TimeVal

select 
    Person.Name + ' ' + Person.FirstName + ' ' + Person.MidName as FIO,
    ISNULL(C.Name, 'Íå çàäàíî') as Company,
    ISNULL(post.Name, 'Íå çàäàíî') as Post,
    plog.TimeVal as StartTime,
    (select top 1 TimeVal from #tmpPLog inplog with(nolock) where inplog.IDComp in (0, 1, 2, 3, 5) and inplog.TimeVal > plog.TimeVal and inplog.TimeVal < DATEADD(day, 2, plog.TimeVal) and inplog.HozOrgan = plog.HozOrgan and inPlog.Mode = 1 and inplog.Event = 28 order by TimeVal) NextStartTime,
    (select top 1 TimeVal from #tmpPLog inplog with(nolock) where inplog.IDComp in (0, 1, 2, 3, 5) and inplog.TimeVal > plog.TimeVal and inplog.TimeVal < DATEADD(day, 2, plog.TimeVal) and inplog.HozOrgan = plog.HozOrgan and inPlog.Mode = 2 and inplog.Event = 28 order by TimeVal) EndTime
into #tmpRes
from pList person with(nolock)
left join pPost post with(nolock) on post.ID = person.Post
left join PCompany C with(nolock) on C.ID = person.Company
left join #tmpPLog plog with(nolock) on 
    plog.HozOrgan = person.ID and plog.Mode = 1 and 
    plog.Event = 28 and 
    TimeVal between @startDate and @endDate
where person.Company <> 1 


select *,
    YEAR(StartTime) SY, MONTH(StartTime)SM, DAY(StartTime) SD,
    YEAR(EndTime) EY, MONTH(EndTime) EM, DAY(EndTime) ED,
    DATEDIFF(HOUR, StartTime, EndTime) Duration
from #tmpRes
where (NextStartTime > EndTime or NextStartTime is null) and EndTime is not null
"""
server = '192.168.24.3'
database = 'orion'
username = 'sa'
password = 'Miha_Artiom'
port = '1434'
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                                   "Server="+server+";"
                                   "Database="+database+";"
                                   "Trusted_Connection=yes;")
cursor=cnxn.cursor()
cursor.execute(sql_query)
print(cursor.fetchall())
cnxn.close()

if __name__ == '__main__':
    pass

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
