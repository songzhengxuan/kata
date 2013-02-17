#include "AddEmployeeTransaction.h"

#include "Employee.h"

AddEmployeeTransaction::AddEmployeeTransaction(int empid, string name, string address) {
	itsEmpid = empid;
	itsName = name;
	itsAddress = address;
}

void AddEmployeeTransaction::Execute() {
	
}
