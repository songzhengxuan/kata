#include "Employee.h"

void Employee::setClassification(PaymentClassification *classification) {
	itsClassification = classification;
}

void Employee::setSchedule(PaymentSchedule *schedule) {
	itsSchedule = schedule;
}

void Employee::setName(string name) {
	itsName = name;
}

void Employee::setAddress(string address) {
	itsAddress = address;
}
