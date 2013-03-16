#ifndef PAYMENTSCHEDULE_H
#define PAYMENTSCHEDULE_H
class PaymentSchedule {
	public:
		virtual ~PaymentSchedule() {}
		virtual bool isPayday(long date) = 0;
};

#endif
