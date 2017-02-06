/**
This program implemtns a GObject for a simple class, then register the object
on the D-Bus and starts serving requests
*/
#include <glib.h>
#include <dbus/dbus-glib.h>
#include <stdlib.h>
#include <unistd.h>

#include "common-defs.h"

typedef enum {
    E_SIGNAL_CHANGED_VALUE1,
    E_SIGNAL_CHANGED_VALUE2,
    E_SIGNAL_OUTOFRANGE_VALUE1,
    E_SIGNAL_OUTOFRANGE_VALUE2,
    E_SIGNAL_COUNT,
} ValueSignalNumber;

/*
This defines the per-instance state.

Each GObject must start with the 'parent' definition so that common
operaitons that all GObjects support can be called on it.
*/
typedef struct {
    /*The parent class object state.*/
    GObject parent;
    /*Our first per-object state variable.*/
    gint value1;
    /*Our second per-object state variable. */
    gdouble value2;
} ValueObject;

/**/
typedef struct {
    GObjectClass parent;
    gint thresholdMin;
    gint thresholdMax;
    guint signals[E_SIGNAL_COUNT];
} ValueObjectClass;

/* Forward declaration of the function that will return the GType of the 
Value implementation. Not used in this program since we only 
need to push this over the D-Bus
*/
GType value_object_get_type(void);

#define VALUE_TYPE_OBJECT (value_object_get_type())

#define VALUE_OBJECT(object) \
    (G_TYUPE_CHECK_INSTANCE_CAST((object), \
    VALUE_TYPE_OBJECT, ValueObject))
#define VALUE_OBJECT_CLASS(kclass) \
    (G_TYPE_CHECK_CLASS_CAST((kclass), \
    VALUE_TYPE_OBJECT, ValueObjectClass))
#define VALUE_IS_OBJECT(object) \
    (G_TYPE_CHECK_INSTANCE_TYPE((object), \
    VALUE_TYPE_OBJECT))
#define VALUE_IS_OBJECT_CLASS(kclass) \
    (G_TYPE_CHECK_CLASS_TYPE((object), \
    VALUE_TYPE_OBJECT))
#define VALUE_OBJECT_GET_CLASS(obj) \
    (G_TYPE_INSTANCE_GET_CLASS((obj), \
    VALUE_TYPE_OBJECT, ValueObjectClass))

/*Utility macro to define the value_object GType structure. */
G_DEFINE_TYPE(ValueObject, value_object, G_TYPE_OBJECT)

/**
Since the stub generator will reference the functions from a call type, 
the functions must be declared before the stub is included
*/
gboolean value_object_getvalue1(ValueObject *obj, gint* value_out,
                                                    GError** error);
gboolean value_object_getvalue2(ValueObject *obj, gdouble* value_out,
                                                    GError** error);
gboolean value_object_setvalue1(ValueObject *obj, gint value_in,
                                                    GError** error);
gboolean value_object_setvalue2(ValueObject *obj, gdouble value_in,
                                                    GError** error);

/*Pudding in the stub for the service side.*/
#include "value-server-stub.h"

#ifdef NO_DAEMON
#define dbg(fmtstr, args...) \
    (g_print(PROGAME ":%s:" fmtstr "\n", __func__, ##args))
#else
#define dbg(dummy...)
#endif

/* Per object initializer*/
static void value_object_init(ValueObject *obj) {
    dbg("Called");
    g_assert(obj != NULL);
    obj->value1 = 0;
    obj->value2 = 0.0;
}

/* Per class initializer */
static void value_object_class_init(ValueObjectClass *klass) {
    const gchar* signalNames[E_SIGNAL_COUNT] = {
        SIGNAL_CHANGED_VALUE1,
        SIGNAL_CHANGED_VALUE2,
        SIGNAL_OUTOFRANGE_VALUE1,
        SIGNAL_OUTOFRANGE_VALUE2};
    int i;
    dbg("Called");
    g_assert(klass != NULL);

    klass->thresholdMin = -100;
    klass->thresholdMax = 100;

    dbg("Creating signals")

    for (i = 0; i < E_SIGNAL_COUNT; ++i) {
        guint signalId;
        signalId = g_signal_new(signalNames[i],
        G_OBJECT_CLASS_TYPE(klass),
        G_SIGNAL_RUN_LAST,
        0,
        NULL,
        NULL,
        g_cclosure_marshal_VOID__STRING,
        G_TYPE_NONE,
        1,
        G_TYPE_STRING);
        klass->signals[i] = signalId;
    }
    dbg("Binding to Glib/D-Bus");

    dbus_g_object_type_install_info(VALUE_TYPE_OBJECT,
        &dbus_glib_value_object_object_info);

    dbg("Done");
}

static void value_object_emitSignal(ValueObject* obj, 
    ValueSignalNumber num, 
    const gchar* message) {
    ValueObjectClass *klass = VALUE_OBJECT_GET_CLASS(obj);
    g_assert((num < E_SIGNAL_COUNT) && (num >= 0));
    dbg("Emitting signal id %d with message %s\n", num, message);
    g_signal_emit(obj, klass->signals[num], 0, message);
}

static gboolean value_object_thresholdsOk(ValueObject* obj, gint value) {
    ValueObjectClass* klass = VALUE_OBJECT_CLASS(obj);
    return ((value  >= klass->thresholdMin) && (value <= klass->thresholdMax));
}

gboolean value_object_setvalue1(ValueObject *obj, gint valueIn, GError** error) {
    dbg("Called (valueIn=%d)", valueIn);
    g_assert(obj != NULL);
    if (obj->value1 != valueIn) {
        obj->value1 = valueIn;
        value_object_emitSignal(obj, E_SIGNAL_CHANGED_VALUE1, "value1");
        if (!value_object_thresholdsOk(obj, valueIn)) {
            value_object_emitSignal(obj, E_SIGNAL_OUTOFRANGE_VALUE1, "value1");
        }
    }
    return TRUE;
}

gboolean value_object_setvalue2(ValueObject *obj, gdouble valueIn, GError** error) {
    dbg("Called (valueIn=%.3f)", valueIn);
    g_assert(obj != NULL);
    if (obj->value2 != valueIn) {
        obj->value2 = valueIn;
        value_object_emitSignal(obj, E_SIGNAL_CHANGED_VALUE2, "value2");
        if (!value_object_thresholdsOk(obj, valueIn)) {
            value_object_emitSignal(obj, E_SIGNAL_OUTOFRANGE_VALUE2, "value2");
        }
    }
    return TRUE;
}

gboolean value_object_getvalue1(ValueObject* obj, gint* valueOut, GError** error) {
    dbg("Called (internal value1 is %d)", obj->value1);
    g_assert(obj != NULL);
    g_assert(valueOut != NULL);
    *valueOut = obj->value1;
}

gboolean value_object_getvalue2(ValueObject* obj, gdouble* valueOut, GError** error) {
    dbg("Called (internal value2 is %.3f)", obj->value2);
    g_assert(obj != NULL);
    g_assert(valueOut != NULL);
    *valueOut = obj->value2;
}

static void handleError(const char* msg, const char *reason, gboolean fatal) {
    g_printerr(PROGNAME ": ERROR: %s (%s)\n", msg, reason);
    if (fatal) {
        exit(EXIT_FAILURE);
    }
}

/**
1. Init GType/GObject
2. Create a mainloop
3. Connect to the session bus
4. Get a proxy object representing the bus itself
5. Register the well-known name by which clients can find ushort
6. Create one Value object that will handle all client requests
7. Register it on the bus(will be found via "/GlobalValue" object path)
8. Daemonize the process(if not built with NO_DAEMON)
9. Start processing requests(run GMainLoop)

This program will not exit(unless it encounts critical errors);
*/
int main(int argc, char **argv) {
    DBusGConnection* bus = NULL;
    DBusGProxy* busProxy = NULL;
    ValueObject *valueObj = NULL;
    GMainLoop* mainloop = NULL;
    guint result;
    GError* error = NULL;

    /*Initialized the GType/Object system.*/
    g_type_init();

    /*Create a main loop that will dispatch callbacks*/
    mainloop = g_main_loop_new(NULL, FALSE);
    if (mainloop == NULL) {
        handleError("Cloudn't create GMainLoop", "Unknown(OOM?)", TRUE);
    }

    g_print(PROGNAME ":main Connecting to the Session D-Bus.\n");
    bus = dbus_g_bus_get(DBUS_BUS_SESSION, &error);
    if (error != NULL) {
        handleError("Couldn't connect to the session D-Bus.\n", error->message, TRUE);
    }

    g_print(PROGNAME ":main Registering the well-known name(%s)\n", VALUE_SERVICE_NAME);

    busProxy = dbus_g_proxy_new_for_name(bus,
        DBUS_SERVICE_DBUS,
        DBUS_PATH_DBUS,
        DBUS_INTERFACE_DBUS);
    if (busProxy == NULL) {
        handleError("Failed to get a proxy for D-Bus", "Unknown(dbus_g_proxy_new_for_name)", TRUE);
    }

    /*Attempt to register the well-known name*/
    if (!dbus_g_proxy_call(busProxy,
        "RequestName",
        &error,
        G_TYPE_STRING,
        VALUE_SERVICE_NAME,
        G_TYPE_UINT,
        0,
        G_TYPE_INVALID,
        G_TYPE_UINT,
        &result,
        G_TYPE_INVALID)) {
        handleError("D-Bus.RequestName RPC failed", error->message, TRUE);
    }
    g_print(PROGNAME ":main RequestName returned %d.\n", result);
    if (result != 1) {
        handleError("Failed to get the primary well-known name.", 
            "Requestname result != 1", TRUE);
    }
    g_print(PROGNAME ":main Creating one Value object.\n");
    valueObj = g_object_new(VALUE_TYPE_OBJECT, NULL);
    if (valueObj == NULL) {
        handleError("Failed to create one Value instance.", 
            "Unknown(OOM?)", TRUE);
    }
    g_print(PROGNAME ":main Registering it on the D-Bus.\n");
    dbus_g_connection_register_g_object(bus,
        VALUE_SERVICE_OBJECT_PATH,
        G_OBJECT(valueObj));
    g_print(PROGNAME ":main Ready to serve requests(damonizing).\n");

#ifndef NO_DAMEON
    if (daemon(0, 0) != 0) {
        g_error(PROGNAME ":Failed to daemonize.\n");
    }
#else
    g_print(PROGANME
        ":Not daemonizing (built with NO_DAEMON-build define)\n");
#endif
    /* Start service requests on the D-Bus forever. */
    g_main_loop_run(mainloop);

    return EXIT_FAILURE;
}
