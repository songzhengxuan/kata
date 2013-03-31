#include "DeleteEmployeeTransaction.h"
#include "PayrollDatabase.h"

extern PayrollDatabase GPayrollDatabase;

DeleteEmployeeTransaction::~DeleteEmployeeTransaction() {
}

DeleteEmployeeTransaction::DeleteEmployeeTransaction(int empid) {
	itsEmpid = empid;
}

void DeleteEmployeeTransaction::Execute() {
	GPayrollDatabase.DeleteEmployee(itsEmpid);
}
