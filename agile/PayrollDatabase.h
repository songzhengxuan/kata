#ifndef PAYROLLDATABASE_H
#define PAYROLLDATABASE_H

#include <map>
using std::map;

class Employee;

class PayrollDatabase {
	public:
		virtual ~PayrollDatabase();
		Employee* GetEmployee(int empId);
		void AddEmployee(int empid, Employee*);
		void DeleteEmployee(int empid);
		void clear() {
			itsEmployees.clear();
		}
	private:
		map<int, Employee*> itsEmployees;
};

extern PayrollDatabase GPayrollDatabase;
#endif 
