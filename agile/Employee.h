#ifndef EMPLOYEE_H
#define EMPLOYEE_H
#include <string>

using std::string;

class PaymentClassification;
class PaymentSchedule;
class PaymentMethod;

class Employee {
	public:
		virtual ~Employee(){};
		Employee(int empid, string name, string address);

		void SetClassification(PaymentClassification *classification);
		PaymentClassification* GetClassification();

		void SetSchedule(PaymentSchedule *schedule);
		PaymentSchedule* GetSchedule();

		void SetName(string name);
		string GetName();

		void SetMethod(PaymentMethod *method);
		PaymentMethod* GetMethod();

		void SetAddress(string address);
		string GetAddress();

	private:
		int itsEmpId;
		string itsName;
		string itsAddress;
		PaymentClassification *itsClassification;
		PaymentSchedule *itsSchedule;
		PaymentMethod *itsMethod;
};
#endif
