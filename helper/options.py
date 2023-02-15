import helper.loadData as ld
import helper.procesing as pr
import helper.workflow as wf
def createWorkSheet(token):
    rw = ld.ChargeRW(token)
    times = ld.chargeTimeLines()
    newCols = wf.rwCreation(rw,times)
    newCols.to_excel('Results\prueba1.xlsx')
    
    