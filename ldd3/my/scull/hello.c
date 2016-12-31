#include <linux/module.h>
#include <linux/moduleparam.h>
#include <linux/init.h>

#include <linux/kernel.h> /* printk() */
#include <linux/slab.h> /*kmalloc()*/
#include <linux/fs.h> /* everything...*/
#include <linux/errno.h> /* error codes */
#include <linux/types.h> /* size_t*/
#include <linux/proc_fs.h>
#include <linux/fcntl.h>
#include <linux/cdev.h>
#include <asm/system.h> /* cli(), *_flags */
#include <asm/uaccess.h> /* copy_*_user */

#include "scull.h"

/*
 * Our paramters which can be set at load time.
 */
int scull_major = SCULL_MAJOR;
int scull_minor = 0;
int scull_nr_devs = SCULL_NR_DEVS;
int scull_quantum = SCULL_QUANTUM;
int scull_qset = SCULL_QSET;

module_param(scull_major, int, S_IRUGO);


MODULE_LICENSE("Dual BSD/GPL");


static int hello_init(void) {
	printk(KERN_ALERT "Hello, world\n");
	return 0;
}

static void hello_exit(void) {
	printk(KERN_ALERT "Goodbye, cruel world\n");
}

int scull_init_module(void) {
	int result, i;
	dev_t dev = 0;
	/* Get a range of minor numbers to work with, asking for a dynamic
	 * major unless directed otherwise at load time.
	 */
	if (scull_major) {
		dev = MKDEV(scull_major, scull_minor);
		result = register_chrdev_region(dev, scull_nr_devs, "scull");
	} else {
		result = alloc_chrdev_region(&dev, scull_minor, scull_nr_devs,
			"scull");
		scull_major = MAJOR(dev);
	}

}

module_init(hello_init);
module_exit(hello_exit);
