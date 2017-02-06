#include <glib.h>
#include <dbus/dbus-glib.h>
#include <stdlib.h>
#include <string.h>

#include "common-defs.h"

#include "value-client-stub.h"

static void handleError(const char*msg, const char* reason, 
    gboolean fatal) {
    g_print(PROGNAME ":Error:%s (%s)\n", msg, reason);
    if (fatal) {
        exit(EXIT_FAILURE);
    }
}

static void outOfRangeSignalHandler(DBusGProxy* proxy,
    const char* valueName,
    gpointer userData) {
    g_print(PROGNAME ":out-of-range (%s)!\n", valueName);
    if (strcmp(valueName, "value1") == 0) {
        g_print(PROGNAME ":out-of-range Value 1 is outside threshold\n");
    } else {
        g_print(PROGNAME ":out-of-range Value 2 is outside threshold\n");
    }
}

static void valueChangedSignalHandler(DBusGProxy *proxy,
    const char* valueName,
    gpointer userData) {
    GError* error = NULL;

    g_print(PROGNAME ":value-chagned (%s)\n", valueName);

    if (strcmp(valueName, "value1") == 0) {
        gint v = 0;
        /* execute the RPC to get value1 */
        org_maemo_Value_getvalue1(proxy, &v, &error);
        if (error == NULL) {
            g_print(PROGNAME ":value-changed Value1 now %d\n", v);
        } else {
            handleError("Failed to retrieve value1", error->message, FALSE);
        }
    } else {
        gdouble v = 0;
        /* execute the RPC to get value1 */
        org_maemo_Value_getvalue2(proxy, &v, &error);
        if (error == NULL) {
            g_print(PROGNAME ":value-changed Value2 now %.3f\n", v);
        } else {
            handleError("Failed to retrieve value2", error->message, FALSE);
        }
    }

    /* Free up error object if one was allocated */
    g_clear_error(&error);
}

/**
*/
static gboolean timerCallback(DBusGProxy* remoteobj) {
    /* Local values that we'll start updating to the remote object */
    static gint localValue1 = -80;
    static gdouble localValue2 = -120.0;

    GError* error = NULL;

    /*Set the first value.*/
    org_maemo_Value_setvalue1(remoteobj, localValue1, &error);
    if (error != NULL) {
        handleError("Failed to set value1", error->message, FALSE);
    } else {
        g_print(PROGNAME ":timerCallback Set value1 to %d\n", localValue1);
    }

    if (error != NULL) {
        g_clear_error(&error);
        return TRUE;
    }

    org_maemo_Value_setvalue2(remoteobj, localValue2, &error);
    if (error != NULL) {
        handleError("Failed to set value2", error->message, FALSE);
        g_clear_error(&error);
    } else {
        g_print(PROGNAME ":timerCallback Set value2 to %.3lf\n", localValue2);
    }

    localValue1 += 10;
    localValue2 += 10.0;

    return TRUE;
}

int main(int argc, char **argv) {
    DBusGConnection* bus;
    DBusGProxy* remoteValue;
    GMainLoop* mainloop;
    GError* error = NULL;

    g_type_init();

    mainloop = g_main_loop_new(NULL, FALSE);
    if (mainloop == NULL) {
        handleError("Failed to create the mainloop", "Unknown (OOM?)", TRUE);
    }

    g_print(PROGNAME ":main Connecting to Session D-Bus.\n");
    bus = dbus_g_bus_get(DBUS_BUS_SESSION, &error);
    if (error != NULL) {
        handleError("Couldn't connect to the Session bus", error->message,
            TRUE);
    }

    g_print(PROGNAME ":main Creating a GLib proxy object for Value.\n");

    remoteValue = 
        dbus_g_proxy_new_for_name(bus, VALUE_SERVICE_NAME,
            VALUE_SERVICE_OBJECT_PATH,
            VALUE_SERVICE_INTERFACE);
    if (remoteValue == NULL) {
        handleError("Couldn't create the proxy object", "Unknown(dbus_g_proxy_new_for_name)", TRUE);
    }

    g_print(PROGNAME ":main Registering signal handler signatures.\n");
    { // create a local scope for variable
        int i;
        const gchar* signalNames[] = {
            SIGNAL_CHANGED_VALUE1,
            SIGNAL_CHANGED_VALUE2,
            SIGNAL_OUTOFRANGE_VALUE1,
            SIGNAL_OUTOFRANGE_VALUE2 
        };
        for (i = 0; i < sizeof(signalNames)/sizeof(signalNames[0]); ++i) {
            dbus_g_proxy_add_signal(
                remoteValue,
                signalNames[i],
                G_TYPE_STRING,
                G_TYPE_INVALID);
        }
    }// end of local scope

    dbus_g_proxy_connect_signal(remoteValue, SIGNAL_CHANGED_VALUE1,
        G_CALLBACK(valueChangedSignalHandler),
         NULL, NULL);
    dbus_g_proxy_connect_signal(remoteValue, SIGNAL_CHANGED_VALUE2,
        G_CALLBACK(valueChangedSignalHandler),
         NULL, NULL);
    dbus_g_proxy_connect_signal(remoteValue, SIGNAL_OUTOFRANGE_VALUE1,
        G_CALLBACK(outOfRangeSignalHandler),
         NULL, NULL);
    dbus_g_proxy_connect_signal(remoteValue, SIGNAL_OUTOFRANGE_VALUE2,
        G_CALLBACK(outOfRangeSignalHandler),
         NULL, NULL);
        
    g_print(PROGNAME ":main Starting main loop (first timer in 1s).\n");

    g_timeout_add(1000, (GSourceFunc)timerCallback, remoteValue);

    g_main_loop_run(mainloop);

    return EXIT_FAILURE;
}

