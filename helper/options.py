import helper.loadData as ld
import helper.procesing as pr
import helper.workflow as wf
def createWorkSheet(token):
    rw = ld.ChargeRW(token)
    times = ld.chargeTimeLines()
    newCols = wf.rwCreation(rw,times)
    pr.create_excel(newCols)
    
    