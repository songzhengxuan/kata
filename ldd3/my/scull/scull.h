#ifndef _SCULL_H_
#define _SCULL_H_

#ifndef SCULL_MAJOR
#define SCULL_MAJOR 0 /* dynamic major by default */
#endif

#ifndef SCULL_NR_DEVS
#define SCULL_NR_DEVS 4
#endif

#ifndef SCULL_QUANTUM
#define SCULL_QUANTUM 4000
#endif

#ifndef SCULL_QSET
#define SCULL_QSET 1000
#endif

struct scull_qset {
	void **data;
	struct scull_qset *next;
};

struct scull_dev {
	struct scull_qset *data; /* Pointer to first quantum set*/
	int quantum; /* the current quantum size*/
	int qset; /* the current array size */
	unsigned long size; /* amount of data stored here */
	unsigned int access_key; /* used by sculluid and scullpriv */
	struct semaphore sem; /* mutual exclusion semaphore */
	struct cdev dev;
};

/*
 * Split minors in two parts
 */
#define TYPE(minor) (((minor) >> 4) & 0xf) /* high nibble*/
#define NUM(minor) ((minor) & 0xf) /* low nibble */

/*
 * The different configurable parameters
 */
extern int scull_major;
extern int scull_nr_devs;
extern int scull_quantum;
extern int scull_qset;



#endif
