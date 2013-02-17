#ifndef EMPLOYEE_H
#define EMPLOYEE_H
#include <string>
using std::string;

class PaymentClassification;
class PaymentSchedule;
class Employee {
	public:
		virtual ~Employee();

		void setClassification(PaymentClassification *classification);

		void setSchedule(PaymentSchedule *schedule);

		void setName(string name);

		void setAddress(string address);

	private:
		PaymentClassification *itsClassification;
		PaymentSchedule *itsSchedule;
		string itsName;
		string itsAddress;
};
#endif
