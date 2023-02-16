import helper.loadData as ld
import helper.procesing as pr
import helper.workflow as wf
def createWorkSheet(token):
    rw = ld.ChargeRW(token)
    times = ld.chargeTimeLines()
    newCols = wf.rwCreation(rw,times)
    pr.create_excel(newCols)

def reviewCof(token):
    sp,cof = pr. PrepareData(token)
    pr.searchdiff(cof,sp)
    