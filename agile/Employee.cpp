#include "Employee.h"

Employee::Employee(int empId, string name, string address) {
	itsEmpId = empId;
	itsName = name;
	itsAddress = address;
}

void Employee::SetClassification(PaymentClassification *classification) {
	itsClassification = classification;
}

PaymentClassification* Employee::GetClassification() {
	return itsClassification;
}

void Employee::SetSchedule(PaymentSchedule *schedule) {
	itsSchedule = schedule;
}

PaymentSchedule* Employee::GetSchedule() {
	return itsSchedule;
}

void Employee::SetName(string name) {
	itsName = name;
}

string Employee::GetName() {
	return itsName;
}

void Employee::SetAddress(string address) {
	itsAddress = address;
}

string Employee::GetAddress() {
	return itsAddress;
}

void Employee::SetMethod(PaymentMethod *method) {
	itsMethod = method;
}

PaymentMethod* Employee::GetMethod() {
	return itsMethod;
}
